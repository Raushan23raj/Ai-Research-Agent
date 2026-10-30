from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.database.postgres import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="AI Research Agent", lifespan=lifespan)

@app.middleware("http")
async def collapse_double_slashes(request, call_next):
    path = request.scope["path"]
    while "//" in path:
        path = path.replace("//", "/")
    request.scope["path"] = path
    return await call_next(request)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://frontend-r1-8d3e.vercel.app",
        "https://ai-research-agent-r1-8d3e.vercel.app",
    ],
    allow_origin_regex=r"https://.*-r1-8d3e\.vercel\.app",
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}