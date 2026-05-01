import argparse
import datetime as dt
import json
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def get_credentials(client_secret_path: Path, token_path: Path) -> Credentials:
    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(client_secret_path), SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json(), encoding="utf-8")
    return creds


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--metadata-json", required=True)
    parser.add_argument("--client-secret", required=True)
    parser.add_argument("--token-path", required=True)
    parser.add_argument("--privacy-status", default="private")
    parser.add_argument("--publish-at", default=None)
    args = parser.parse_args()

    metadata = json.loads(Path(args.metadata_json).read_text(encoding="utf-8"))
    creds = get_credentials(Path(args.client_secret), Path(args.token_path))
    youtube = build("youtube", "v3", credentials=creds)

    status = {"privacyStatus": args.privacy_status}
    if args.publish_at:
        publish_at = dt.datetime.fromisoformat(args.publish_at)
        status["publishAt"] = publish_at.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat()

    body = {
        "snippet": {
            "title": metadata["title"],
            "description": metadata["description"],
            "tags": metadata.get("tags", []),
            "categoryId": metadata.get("categoryId", "10"),
        },
        "status": status,
    }

    media = MediaFileUpload(args.video, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    print(f"uploaded video id: {response['id']}")


if __name__ == "__main__":
    main()
