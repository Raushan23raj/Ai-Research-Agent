import { AGENTS } from "../hooks/useResearch";

export default function AgentProgress({ completed, loading }) {
  const currentIndex = completed.length;

  return (
    <div className="progress">
      {AGENTS.map((agent, i) => {
        let status = "pending";
        if (completed.includes(agent.key)) status = "done";
        else if (loading && i === currentIndex) status = "running";

        return (
          <div key={agent.key} className={`step ${status}`}>
            <span className="dot" />
            {agent.label}
          </div>
        );
      })}
    </div>
  );
}