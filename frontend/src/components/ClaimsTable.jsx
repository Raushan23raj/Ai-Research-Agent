export default function ClaimsTable({ claims }) {
  if (!claims || claims.length === 0) return null;

  return (
    <section className="card">
      <h2>Fact Check</h2>
      <table>
        <thead>
          <tr>
            <th>Claim</th>
            <th>Verdict</th>
            <th>Confidence</th>
            <th>Sources</th>
          </tr>
        </thead>
        <tbody>
          {claims.map((c, i) => (
            <tr key={i}>
              <td>{c.claim}</td>
              <td>
                <span className={`badge ${c.verdict}`}>
                  {c.verdict.replace("_", " ")}
                </span>
              </td>
              <td>{Math.round(c.confidence * 100)}%</td>
              <td>{c.source_indices.map((n) => `[${n}]`).join(" ")}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}