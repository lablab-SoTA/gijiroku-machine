from datetime import timedelta
from typing import List, Optional
from pydantic import BaseModel, Field


class SpeakerSegment(BaseModel):
    """Represents a diarized segment in the meeting transcript."""

    speaker: str = Field(..., description="Speaker label assigned by GPT-4o.")
    start: float = Field(..., ge=0.0, description="Start time in seconds.")
    end: float = Field(..., ge=0.0, description="End time in seconds.")
    text: str = Field(..., description="Transcribed utterance for the segment.")


class TranscriptMetadata(BaseModel):
    """High-level metadata summarizing the diarized transcript."""

    language: str = Field(..., description="Detected or requested language code (e.g., 'ja').")
    duration: float = Field(..., ge=0.0, description="Duration of the processed audio in seconds.")
    summary: Optional[str] = Field(default=None, description="Optional LLM-generated summary.")


class TranscriptionResponse(BaseModel):
    """Unified response payload returned by the transcription endpoint."""

    segments: List[SpeakerSegment]
    metadata: TranscriptMetadata


class TranscriptionJob(BaseModel):
    """Client payload describing diarization preferences."""

    language: str = Field(default="ja", description="Hint language for transcription.")
    summarize: bool = Field(default=True, description="Whether to request a short meeting summary.")
