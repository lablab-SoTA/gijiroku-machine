import { useMutation, UseMutationOptions } from "@tanstack/react-query";
import { postTranscription, TranscriptionPayload, TranscriptionResponse } from "../lib/api";

export function useUploadTranscription(
  options?: UseMutationOptions<TranscriptionResponse, Error, TranscriptionPayload>
) {
  return useMutation<TranscriptionResponse, Error, TranscriptionPayload>({
    mutationFn: postTranscription,
    ...options
  });
}
