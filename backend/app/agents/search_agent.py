from app.services.search import web_search
from app.graph.state import ResearchState

def search_agent(state: ResearchState):
    sources = web_search(state["query"])
    return {"sources": sources}