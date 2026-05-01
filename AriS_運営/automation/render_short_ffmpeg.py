import argparse
import subprocess
from pathlib import Path


def run_ffmpeg(input_video: Path, output_video: Path, title_text: str, ffmpeg_bin: str) -> None:
    output_video.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        ffmpeg_bin,
        "-y",
        "-i",
        str(input_video),
        "-vf",
        (
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,"
            f"drawtext=text='{title_text}':"
            "x=(w-text_w)/2:y=80:fontsize=56:fontcolor=white:box=1:boxcolor=black@0.5:boxborderw=14"
        ),
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "21",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-af",
        "loudnorm",
        str(output_video),
    ]
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--song", required=True)
    parser.add_argument("--input-video", required=True)
    parser.add_argument("--output-video", required=True)
    parser.add_argument("--ffmpeg-bin", default="ffmpeg")
    args = parser.parse_args()

    run_ffmpeg(
        input_video=Path(args.input_video),
        output_video=Path(args.output_video),
        title_text=f"{args.song} / AriS",
        ffmpeg_bin=args.ffmpeg_bin,
    )
    print(f"short video created: {args.output_video}")


if __name__ == "__main__":
    main()
