import axios from "axios";

export type TranscriptionPayload = {
  file: File;
  language: string;
  summarize: boolean;
};

export type TranscriptionResponse = {
  metadata: {
    language: string;
    duration: number;
    summary?: string | null;
  };
  segments: Array<{
    speaker: string;
    start: number;
    end: number;
    text: string;
  }>;
};

export async function postTranscription(payload: TranscriptionPayload): Promise<TranscriptionResponse> {
  const formData = new FormData();
  formData.append("file", payload.file);
  formData.append("language", payload.language);
  formData.append("summarize", String(payload.summarize));

  const response = await axios.post<TranscriptionResponse>("/transcriptions/", formData, {
    headers: { "Content-Type": "multipart/form-data" },
    timeout: 600_000
  });

  return response.data;
}
