import argparse
import json
from pathlib import Path


def make_metadata(song: str, tags: list[str]) -> dict:
    title = f"{song} / AriS【Lyric Video】"
    description = f"{song} Lyric Video\nAriS\n\n#AriS #{song} #LyricVideo"
    return {
        "title": title,
        "description": description,
        "tags": tags + [song],
        "categoryId": "10",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--song", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--tags", nargs="*", default=[])
    args = parser.parse_args()

    payload = make_metadata(args.song, args.tags)
    out = Path(args.output_json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"metadata created: {out}")


if __name__ == "__main__":
    main()
