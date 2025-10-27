#!/usr/bin/env python
"""Upload a sample audio file to the running API for quick verification."""

from __future__ import annotations

import argparse
from pathlib import Path

import requests


def main() -> None:
    parser = argparse.ArgumentParser(description="Send an audio file to the diarization API.")
    parser.add_argument("--input", required=True, help="Path to the audio file (wav/mp3/m4a/mp4).")
    parser.add_argument("--lang", default="ja", help="Language hint for transcription (default: ja).")
    parser.add_argument(
        "--url",
        default="http://localhost:8000/transcriptions/",
        help="Transcription endpoint URL.",
    )
    args = parser.parse_args()

    audio_path = Path(args.input)
    if not audio_path.exists():
        raise SystemExit(f"Audio file not found: {audio_path}")

    with audio_path.open("rb") as audio_file:
        files = {"file": (audio_path.name, audio_file, "application/octet-stream")}
        data = {"language": args.lang, "summarize": "true"}
        response = requests.post(args.url, data=data, files=files, timeout=600)

    response.raise_for_status()
    print(response.json())


if __name__ == "__main__":
    main()
