export default function SourcesList({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <section className="card">
      <h2>Sources</h2>
      <ol className="sources">
        {sources.map((s) => (
          <li key={s.index} value={s.index}>
            <a href={s.url} target="_blank" rel="noreferrer">
              {s.title}
            </a>
          </li>
        ))}
      </ol>
    </section>
  );
}