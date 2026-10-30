from langgraph.graph import StateGraph, START, END
from app.graph.state import ResearchState
from app.agents.search_agent import search_agent
from app.agents.research_agent import research_agent
from app.agents.fact_checker import fact_checker_agent
from app.agents.analyst import analyst_agent
from app.agents.report_generator import report_agent

graph = StateGraph(ResearchState)

graph.add_node("search", search_agent)
graph.add_node("retrieval", research_agent)
graph.add_node("fact_check", fact_checker_agent)
graph.add_node("analysis", analyst_agent)
graph.add_node("report", report_agent)

graph.add_edge(START, "search")
graph.add_edge("search", "retrieval")
graph.add_edge("retrieval", "fact_check")
graph.add_edge("fact_check", "analysis")
graph.add_edge("analysis", "report")
graph.add_edge("report", END)

research_graph = graph.compile()