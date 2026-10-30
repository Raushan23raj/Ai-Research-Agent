from app.services.llm import llm
from app.graph.state import ResearchState

def report_agent(state: ResearchState):
    source_list = "\n".join(
        f"[{s['index']}] {s['title']} - {s['url']}" for s in state["sources"]
    )
    prompt = (
        f"Write a structured markdown research report answering: {state['query']}\n\n"
        f"Analysis to base it on:\n{state['analysis']}\n\n"
        "Format: Title, Summary, Key Findings, Discussion, Limitations, Sources. "
        "Cite claims inline as [1], [2]. Use only the analysis provided.\n\n"
        f"Source list:\n{source_list}"
    )
    return {"report": llm.invoke(prompt).content}