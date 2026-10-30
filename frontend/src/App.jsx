import { useState, useCallback } from "react";
import useResearch from "./hooks/useResearch";
import { getSession } from "./services/api";
import QueryForm from "./components/QueryForm";
import AgentProgress from "./components/AgentProgress";
import ReportView from "./components/ReportView";
import ClaimsTable from "./components/ClaimsTable";
import SourcesList from "./components/SourcesList";
import SessionHistory from "./components/SessionHistory";

export default function App() {
  const [refreshKey, setRefreshKey] = useState(0);
  const onFinished = useCallback(() => setRefreshKey((k) => k + 1), []);
  const { completed, result, loading, error, start, showSaved, reset } =
    useResearch(onFinished);

  const openSession = async (id) => {
    try {
      const session = await getSession(id);
      showSaved(session);
    } catch {
      /* ignore */
    }
  };

  const handleDeleted = (id) => {
    if (id === null || result?.id === id) reset();
    setRefreshKey((k) => k + 1);
  };

  return (
    <div className="layout">
      <SessionHistory
        refreshKey={refreshKey}
        onSelect={openSession}
        onDeleted={handleDeleted}
      />

      <main className="main">
        <h1>AI Research Agent</h1>
        <p className="muted">
          Multi-agent research with fact-checking and cited reports
        </p>

        <QueryForm onSubmit={start} loading={loading} />

        {(loading || result) && (
          <AgentProgress completed={completed} loading={loading} />
        )}

        {error && <div className="error">{error}</div>}

        {result && (
          <>
            <ReportView report={result.report} />
            <ClaimsTable claims={result.claims} />
            <SourcesList sources={result.sources} />
          </>
        )}
      </main>
    </div>
  );
}