import tempfile
from typing import Optional

from fastapi import UploadFile
from openai import OpenAI

from app.core.config import Settings
from app.schemas.transcription import (
    SpeakerSegment,
    TranscriptMetadata,
    TranscriptionJob,
    TranscriptionResponse,
)


class TranscriptionService:
    """Coordinates GPT-4o Transcribe Diariz requests and formatting."""

    _SUPPORTED_MIME_TYPES = {
        "audio/wav",
        "audio/x-wav",
        "audio/mpeg",
        "audio/mp3",
        "audio/mp4",
        "audio/x-m4a",
        "video/mp4",
        "application/octet-stream",
    }

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def transcribe(self, upload_file: UploadFile, job: TranscriptionJob) -> TranscriptionResponse:
        """Upload audio, request diarized transcript, and return structured response."""
        api_key = self._get_api_key()
        safe_bytes = await upload_file.read()
        await upload_file.close()

        self._validate_size(len(safe_bytes))
        self._validate_mime(upload_file)

        with tempfile.NamedTemporaryFile(suffix=f"_{upload_file.filename or 'audio'}", delete=True) as tmp:
            tmp.write(safe_bytes)
            tmp.flush()
            client = OpenAI(api_key=api_key)
            transcript = self._request_transcription(client=client, path=tmp.name, job=job)
            summary = self._maybe_summarize(client=client, transcript=transcript, job=job)

        segments = [
            SpeakerSegment(
                speaker=segment.get("speaker", f"Speaker {index + 1}"),
                start=float(segment.get("start", 0.0)),
                end=float(segment.get("end", 0.0)),
                text=segment.get("text", "").strip(),
            )
            for index, segment in enumerate(transcript.get("segments", []))
        ]
        duration = float(transcript.get("duration", segments[-1].end if segments else 0.0))

        return TranscriptionResponse(
            segments=segments,
            metadata=TranscriptMetadata(
                language=transcript.get("language", job.language),
                duration=duration,
                summary=summary,
            ),
        )

    def _validate_size(self, size_bytes: int) -> None:
        limit = self.settings.max_upload_mb * 1024 * 1024
        if size_bytes > limit:
            raise ValueError("アップロードされたファイルがサイズ上限を超えています。200MB 以下にしてください。")

    def _validate_mime(self, upload_file: UploadFile) -> None:
        if upload_file.content_type not in self._SUPPORTED_MIME_TYPES:
            raise ValueError("サポートされていないファイル形式です。wav/mp3/m4a/mp4 を使用してください。")

    def _get_api_key(self) -> str:
        if not self.settings.openai_api_key:
            raise ValueError("APP_OPENAI_API_KEY を設定してください。")
        return self.settings.openai_api_key.get_secret_value()

    def _request_transcription(self, client: OpenAI, path: str, job: TranscriptionJob) -> dict:
        """Invoke GPT-4o Transcribe Diariz and return its raw response as a dict."""
        with open(path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model=self.settings.openai_model,
                file=audio_file,
                language=job.language,
                response_format="verbose_json",
                diarize=True,
            )

        # OpenAI returns a pydantic-like object; convert to plain dict for downstream usage.
        return response.to_dict() if hasattr(response, "to_dict") else dict(response)

    def _maybe_summarize(
        self,
        client: OpenAI,
        transcript: dict,
        job: TranscriptionJob,
    ) -> Optional[str]:
        """Request a brief summary when desired."""
        if not job.summarize:
            return None

        segments = transcript.get("segments", [])
        transcript_text = "\n".join(
            f"{segment.get('speaker', 'Speaker')} ({segment.get('start', 0):.1f}-{segment.get('end', 0):.1f}): "
            f"{segment.get('text', '').strip()}"
            for segment in segments
        )
        if not transcript_text:
            return None

        prompt = (
            "以下は会議の発言ログです。主要な決定事項、宿題、懸念点を日本語で簡潔に3-5行で要約してください。\n\n"
            f"{transcript_text}"
        )
        summary_response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {"role": "system", "content": "You produce concise Japanese meeting minutes."},
                {"role": "user", "content": prompt},
            ],
            max_output_tokens=300,
        )

        return _extract_text(summary_response)


def _extract_text(response: object) -> Optional[str]:
    """Best-effort extraction of text from the Responses API output."""
    if response is None:
        return None

    # Newer openai SDK objects expose `output_text`.
    text = getattr(response, "output_text", None)
    if isinstance(text, str) and text.strip():
        return text.strip()

    # Fallback: traverse the output structure.
    output = getattr(response, "output", None)
    if not output:
        return None

    collected: list[str] = []
    for item in output:
        contents = getattr(item, "content", []) or item.get("content", [])  # type: ignore[attr-defined]
        for content in contents:
            if isinstance(content, dict) and content.get("type") == "output_text":
                collected.append(content.get("text", "").strip())
            elif hasattr(content, "text"):
                collected.append(str(content.text).strip())

    return "\n".join(filter(None, collected)) or None
