import pytest

from app.core.config import Settings
from app.schemas.transcription import TranscriptionJob
from app.services.transcribe import TranscriptionService


class DummyUploadFile:
    def __init__(self, data: bytes, filename: str = "sample.wav", content_type: str = "audio/wav") -> None:
        self._data = data
        self.filename = filename
        self.content_type = content_type

    async def read(self) -> bytes:
        return self._data

    async def close(self) -> None:
        return None


@pytest.mark.asyncio
async def test_transcribe_builds_segments_and_summary(monkeypatch):
    settings = Settings(
        openai_api_key="sk-test",
        openai_model="gpt-4o-transcribe-diariz",
    )
    service = TranscriptionService(settings=settings)

    dummy_response = {
        "language": "ja",
        "duration": 12.0,
        "segments": [
            {"speaker": "A", "start": 0.0, "end": 5.0, "text": "おはようございます。"},
            {"speaker": "B", "start": 5.0, "end": 12.0, "text": "議題に入りましょう。"},
        ],
    }

    def fake_transcribe(**_: object) -> dict:
        return dummy_response

    def fake_summary(**_: object) -> str:
        return "主要な議題: プロジェクト開始。次回までの宿題あり。"

    monkeypatch.setattr(service, "_request_transcription", lambda client, path, job: fake_transcribe())
    monkeypatch.setattr(service, "_maybe_summarize", lambda client, transcript, job: fake_summary())
    monkeypatch.setattr(service, "_get_api_key", lambda: "sk-test")

    data = b"FAKEAUDIO"
    upload = DummyUploadFile(data=data)
    job = TranscriptionJob(language="ja", summarize=True)

    result = await service.transcribe(upload, job)

    assert result.metadata.language == "ja"
    assert len(result.segments) == 2
    assert result.metadata.summary.startswith("主要な議題")
