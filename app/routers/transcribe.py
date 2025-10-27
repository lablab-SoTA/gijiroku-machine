from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from starlette import status

from app.core.config import Settings, get_settings
from app.schemas.transcription import TranscriptionJob, TranscriptionResponse
from app.services.transcribe import TranscriptionService


router = APIRouter(prefix="/transcriptions", tags=["transcriptions"])


def _get_service(settings: Settings = Depends(get_settings)) -> TranscriptionService:
    return TranscriptionService(settings=settings)


@router.post(
    "/",
    response_model=TranscriptionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Transcribe and diarize an uploaded meeting recording.",
)
async def create_transcription(
    payload: TranscriptionJob = Depends(),
    file: UploadFile = File(..., description="Audio file to transcribe (wav, mp3, m4a, mp4)."),
    service: TranscriptionService = Depends(_get_service),
) -> TranscriptionResponse:
    try:
        return await service.transcribe(upload_file=file, job=payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
