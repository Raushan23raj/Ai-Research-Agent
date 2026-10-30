from app.services.llm import llm
from app.graph.state import ResearchState

def analyst_agent(state: ResearchState):
    usable = [c for c in state["claims"] if c["verdict"] != "unsupported"]
    claims_text = "\n".join(
        f"- {c['claim']} (sources {c['source_indices']}, confidence {c['confidence']})"
        for c in usable
    )
    prompt = (
        f"Question: {state['query']}\n\n"
        f"Verified claims:\n{claims_text}\n\n"
        "Synthesize these into an analysis: key findings, points where sources "
        "agree, and any gaps or conflicts. Keep source numbers next to each point. "
        "Do not add facts that are not in the claims."
    )
    return {"analysis": llm.invoke(prompt).content}