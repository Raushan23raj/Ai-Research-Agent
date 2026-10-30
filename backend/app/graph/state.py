from typing import TypedDict

class ResearchState(TypedDict, total=False):
    session_id: int
    query: str
    sources: list[dict]    # from Search Agent
    evidence: list[dict]   # from Research Agent
    claims: list[dict]     # from Fact Checker
    analysis: str          # from Analyst
    report: str            # from Report Generator