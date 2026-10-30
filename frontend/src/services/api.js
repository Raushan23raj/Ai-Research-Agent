const API =
  import.meta.env.VITE_API_URL || "https://ai-research-agent-1-zuz2.onrender.com";
const BASE = API.replace(/\/+$/, "");

export function streamUrl(query) {
  return `${BASE}/research/stream?query=${encodeURIComponent(query)}`;
}

export async function listSessions() {
  const res = await fetch(`${BASE}/sessions`);
  if (!res.ok) throw new Error("Could not load sessions");
  return res.json();
}

export async function getSession(id) {
  const res = await fetch(`${BASE}/sessions/${id}`);
  if (!res.ok) throw new Error("Could not load session");
  return res.json();
}

export async function deleteSession(id) {
  const res = await fetch(`${BASE}/sessions/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Could not delete session");
  return res.json();
}

export async function deleteAllSessions() {
  const res = await fetch(`${BASE}/sessions`, { method: "DELETE" });
  if (!res.ok) throw new Error("Could not delete sessions");
  return res.json();
}