import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy import select
from app.database.postgres import SessionLocal, ResearchSession
from app.graph.workflow import research_graph
from sqlalchemy import select, delete
from app.database.postgres import SessionLocal, ResearchSession, Chunk


router = APIRouter()

class Query(BaseModel):
    query: str

def run_pipeline(query: str):
    """Runs the graph, saves the session, and yields (event_name, data)."""
    with SessionLocal() as db:
        session = ResearchSession(query=query)
        db.add(session)
        db.commit()
        db.refresh(session)

        state = {"session_id": session.id, "query": query}
        try:
            for update in research_graph.stream(state, stream_mode="updates"):
                for node, output in update.items():
                    state.update(output)
                    yield node, None

            session.report = state["report"]
            session.claims = state["claims"]
            session.sources = state["sources"]
            session.status = "done"
            db.commit()
            yield "done", {
                "id": session.id,
                "report": state["report"],
                "claims": state["claims"],
                "sources": state["sources"],
            }
        except Exception as e:
            session.status = "failed"
            db.commit()
            yield "error", {"detail": str(e)}

@router.post("/research")
def research(body: Query):
    for event, data in run_pipeline(body.query):
        if event == "error":
            raise HTTPException(status_code=500, detail=data["detail"])
        if event == "done":
            return data

@router.get("/research/stream")
def research_stream(query: str):
    def events():
        for event, data in run_pipeline(query):
            payload = {"agent": event, **(data or {})}
            yield f"data: {json.dumps(payload)}\n\n"
    return StreamingResponse(events(), media_type="text/event-stream")

@router.get("/sessions")
def list_sessions():
    with SessionLocal() as db:
        rows = db.scalars(
            select(ResearchSession).order_by(ResearchSession.id.desc())
        ).all()
        return [
            {"id": r.id, "query": r.query, "status": r.status, "created_at": r.created_at}
            for r in rows
        ]

@router.get("/sessions/{session_id}")
def get_session(session_id: int):
    with SessionLocal() as db:
        r = db.get(ResearchSession, session_id)
        if not r:
            raise HTTPException(status_code=404, detail="Session not found")
        return {
            "id": r.id,
            "query": r.query,
            "status": r.status,
            "report": r.report,
            "claims": r.claims,
            "sources": r.sources,
        }

@router.delete("/sessions/{session_id}")
def delete_session(session_id: int):
    with SessionLocal() as db:
        r = db.get(ResearchSession, session_id)
        if not r:
            raise HTTPException(status_code=404, detail="Session not found")
        db.delete(r)  # its chunks are deleted too (cascade)
        db.commit()
        return {"deleted": session_id}

@router.delete("/sessions")
def delete_all_sessions():
    with SessionLocal() as db:
        db.execute(delete(Chunk))
        count = db.execute(delete(ResearchSession)).rowcount
        db.commit()
        return {"deleted": count}