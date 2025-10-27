import { useState } from "react";
import { useUploadTranscription } from "./hooks/useUpload";
import { SegmentList } from "./components/SegmentList";
import { SummaryCard } from "./components/SummaryCard";

type StatusMessage = {
  type: "idle" | "uploading" | "error";
  message: string;
};

const initialStatus: StatusMessage = { type: "idle", message: "音声ファイルをアップロードしてください。" };

function App(): JSX.Element {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<StatusMessage>(initialStatus);

  const { mutate, data, isPending } = useUploadTranscription({
    onMutate: () => setStatus({ type: "uploading", message: "アップロード中..." }),
    onSuccess: () => setStatus({ type: "idle", message: "完了しました。" }),
    onError: (error: Error) => setStatus({ type: "error", message: error.message }),
  });

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file) {
      setStatus({ type: "error", message: "ファイルを選択してください。" });
      return;
    }
    mutate({ file, language: "ja", summarize: true });
  };

  return (
    <div className="layout">
      <header>
        <h1>ぎじろくさくせい</h1>
        <p>GPT-4o Transcribe Diariz で会議録を自動生成します。</p>
      </header>
      <main>
        <section className="card">
          <form className="form" onSubmit={handleSubmit}>
            <label className="file-field">
              <span>音声ファイル (wav, mp3, m4a, mp4) を選択</span>
              <input
                type="file"
                accept=".wav,.mp3,.m4a,.mp4,audio/*,video/mp4"
                onChange={(event) => setFile(event.target.files?.[0] ?? null)}
              />
            </label>
            <button type="submit" disabled={!file || isPending}>
              {isPending ? "処理中..." : "アップロードして要約"}
            </button>
            <p className={`status status-${status.type}`}>{status.message}</p>
          </form>
        </section>
        {data && (
          <section className="grid">
            <SummaryCard summary={data.metadata.summary} />
            <SegmentList segments={data.segments} />
          </section>
        )}
      </main>
      <footer>APIキーはバックエンドの `.env.local` に設定してください。</footer>
    </div>
  );
}

export default App;
