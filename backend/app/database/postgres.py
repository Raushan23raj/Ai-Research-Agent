from datetime import datetime
from sqlalchemy import create_engine, text, String, Text, JSON, ForeignKey, DateTime
from sqlalchemy.orm import (sessionmaker, DeclarativeBase, Mapped,
                            mapped_column, relationship)
from pgvector.sqlalchemy import Vector
from app.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)

class Base(DeclarativeBase):
    pass

class ResearchSession(Base):
    __tablename__ = "research_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    query: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="running")
    report: Mapped[str | None] = mapped_column(Text, nullable=True)
    claims: Mapped[list | None] = mapped_column(JSON, nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    chunks: Mapped[list["Chunk"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )

class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("research_sessions.id"))
    source_index: Mapped[int]
    url: Mapped[str] = mapped_column(Text)
    text: Mapped[str] = mapped_column(Text)
    embedding = mapped_column(Vector(1536))

    session: Mapped["ResearchSession"] = relationship(back_populates="chunks")

def init_db():
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    Base.metadata.create_all(engine)