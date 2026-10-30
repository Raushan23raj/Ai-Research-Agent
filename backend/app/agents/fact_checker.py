from typing import Literal
from pydantic import BaseModel
from app.services.llm import llm
from app.graph.state import ResearchState

class Claim(BaseModel):
    claim: str
    verdict: Literal["supported", "partially_supported", "unsupported"]
    source_indices: list[int]
    confidence: float  # 0 to 1

class ClaimList(BaseModel):
    claims: list[Claim]

checker = llm.with_structured_output(ClaimList)

def fact_checker_agent(state: ResearchState):
    evidence = "\n\n".join(
        f"[{e['source_index']}] {e['text']}" for e in state["evidence"]
    )
    prompt = (
        f"Question: {state['query']}\n\n"
        "From the evidence below, extract the 5-8 most important factual claims "
        "that help answer the question. For each claim, check whether the evidence "
        "supports it, list the source numbers that support it, and give a "
        "confidence from 0 to 1. Claims backed by multiple independent sources "
        "deserve higher confidence. Mark a claim 'unsupported' if no evidence "
        "backs it.\n\n"
        f"Evidence:\n{evidence}"
    )
    result = checker.invoke(prompt)
    return {"claims": [c.model_dump() for c in result.claims]}