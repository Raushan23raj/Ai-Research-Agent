from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy import select
from app.services.llm import embedder
from app.database.postgres import SessionLocal, Chunk
from app.graph.state import ResearchState

splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)

def research_agent(state: ResearchState):
    texts, meta = [], []
    for s in state["sources"]:
        for piece in splitter.split_text(s["content"]):
            texts.append(piece)
            meta.append((s["index"], s["url"]))

    if not texts:
        return {"evidence": []}

    vectors = embedder.embed_documents(texts)
    query_vec = embedder.embed_query(state["query"])

    with SessionLocal() as db:
        for text_, (idx, url), vec in zip(texts, meta, vectors):
            db.add(Chunk(
                session_id=state["session_id"],
                source_index=idx,
                url=url,
                text=text_,
                embedding=vec,
            ))
        db.commit()

        stmt = (
            select(Chunk)
            .where(Chunk.session_id == state["session_id"])
            .order_by(Chunk.embedding.cosine_distance(query_vec))
            .limit(8)
        )
        top = db.scalars(stmt).all()
        evidence = [
            {"source_index": c.source_index, "url": c.url, "text": c.text}
            for c in top
        ]

    return {"evidence": evidence}