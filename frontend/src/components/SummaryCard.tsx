type Props = {
  summary: string | null | undefined;
};

export function SummaryCard({ summary }: Props): JSX.Element {
  return (
    <section className="card">
      <h2>要約</h2>
      {summary ? (
        <p className="summary-text">{summary}</p>
      ) : (
        <p className="summary-empty">要約は利用できません。</p>
      )}
    </section>
  );
}
