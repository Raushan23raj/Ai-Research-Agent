import { useState, useRef, useCallback } from "react";
import { streamUrl } from "../services/api";

export const AGENTS = [
  { key: "search", label: "Search" },
  { key: "retrieval", label: "Retrieval" },
  { key: "fact_check", label: "Fact Check" },
  { key: "analysis", label: "Analysis" },
  { key: "report", label: "Report" },
];

export default function useResearch(onFinished) {
  const [completed, setCompleted] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const sourceRef = useRef(null);

  const start = useCallback(
    (query) => {
      if (sourceRef.current) sourceRef.current.close();
      setCompleted([]);
      setResult(null);
      setError(null);
      setLoading(true);

      const es = new EventSource(streamUrl(query));
      sourceRef.current = es;

      es.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.agent === "done") {
          setResult(data);
          setLoading(false);
          es.close();
          if (onFinished) onFinished();
        } else if (data.agent === "error") {
          setError(data.detail);
          setLoading(false);
          es.close();
        } else {
          setCompleted((prev) => [...prev, data.agent]);
        }
      };

      es.onerror = () => {
        setError("Connection to the backend failed. Is the server running?");
        setLoading(false);
        es.close();
      };
    },
    [onFinished]
  );

  const showSaved = useCallback((session) => {
    setCompleted(AGENTS.map((a) => a.key));
    setResult(session);
    setError(null);
  }, []);
  
  const reset = useCallback(() => {
    if (sourceRef.current) sourceRef.current.close();
    setCompleted([]);
    setResult(null);
    setError(null);
    setLoading(false);
  }, []);

    return { completed, result, loading, error, start, showSaved, reset };
}