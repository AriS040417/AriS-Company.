import argparse
import json
import subprocess
import sys
from pathlib import Path


def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        raise FileNotFoundError(f"missing config: {config_path}")
    return json.loads(config_path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--song", required=True)
    parser.add_argument("--input-video", required=True)
    parser.add_argument("--publish-at", default=None, help="ISO8601, e.g. 2026-05-02T12:00:00+09:00")
    parser.add_argument("--config", default="automation/config.json")
    parser.add_argument("--upload", action="store_true")
    args = parser.parse_args()

    cfg = load_config(Path(args.config))
    output_root = Path(cfg["output_root"])
    shorts_dir = output_root / "shorts"
    youtube_dir = output_root / "youtube"
    base_name = f"{args.song}_lyric"

    video_path = shorts_dir / f"{base_name}.mp4"
    metadata_path = youtube_dir / f"{base_name}.json"

    ffmpeg_bin = cfg.get("ffmpeg_path", "ffmpeg")

    subprocess.run(
        [
            sys.executable,
            "automation/render_short_ffmpeg.py",
            "--song",
            args.song,
            "--input-video",
            args.input_video,
            "--output-video",
            str(video_path),
            "--ffmpeg-bin",
            ffmpeg_bin,
        ],
        check=True,
    )

    subprocess.run(
        [
            sys.executable,
            "automation/generate_metadata.py",
            "--song",
            args.song,
            "--output-json",
            str(metadata_path),
            "--tags",
            *cfg.get("default_tags", []),
        ],
        check=True,
    )

    print(f"video: {video_path}")
    print(f"metadata: {metadata_path}")

    if args.upload:
        subprocess.run(
            [
                sys.executable,
                "automation/upload_youtube.py",
                "--video",
                str(video_path),
                "--metadata-json",
                str(metadata_path),
                "--client-secret",
                cfg["youtube_client_secret_path"],
                "--token-path",
                cfg["youtube_token_path"],
                "--privacy-status",
                cfg.get("default_privacy_status", "private"),
                *(["--publish-at", args.publish_at] if args.publish_at else []),
            ],
            check=True,
        )


if __name__ == "__main__":
    main()
