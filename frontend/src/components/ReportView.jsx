import ReactMarkdown from "react-markdown";

export default function ReportView({ report }) {
  return (
    <section className="card">
      <h2>Report</h2>
      <div className="markdown">
        <ReactMarkdown>{report}</ReactMarkdown>
      </div>
    </section>
  );
}