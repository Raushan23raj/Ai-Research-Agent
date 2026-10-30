import { useEffect, useState } from "react";
import { listSessions, deleteSession, deleteAllSessions } from "../services/api";

export default function SessionHistory({ refreshKey, onSelect, onDeleted }) {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    listSessions().then(setSessions).catch(() => setSessions([]));
  }, [refreshKey]);

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this research session?")) return;
    try {
      await deleteSession(id);
      onDeleted(id);
    } catch {
      alert("Could not delete the session.");
    }
  };

  const handleDeleteAll = async () => {
    if (!window.confirm("Delete ALL history? This cannot be undone.")) return;
    try {
      await deleteAllSessions();
      onDeleted(null);
    } catch {
      alert("Could not delete the history.");
    }
  };

  return (
    <aside className="history">
      <div className="history-head">
        <h3>History</h3>
        {sessions.length > 0 && (
          <button className="clear-all" onClick={handleDeleteAll}>
            Clear all
          </button>
        )}
      </div>

      {sessions.length === 0 && <p className="muted">No sessions yet</p>}

      <ul>
        {sessions.map((s) => (
          <li key={s.id} className="history-item">
            <button
              className="open"
              onClick={() => onSelect(s.id)}
              disabled={s.status !== "done"}
              title={s.query}
            >
              {s.query}
            </button>
            <button
              className="del"
              onClick={() => handleDelete(s.id)}
              title="Delete"
              aria-label="Delete session"
            >
              ✕
            </button>
          </li>
        ))}
      </ul>
    </aside>
  );
}