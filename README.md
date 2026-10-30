# AI Research Agent

A multi-agent research assistant. Ask a question, and five specialized agents search the web, retrieve the most relevant evidence, fact-check the key claims, analyze them, and write a structured report with numbered source citations.

Built with FastAPI, LangGraph, PostgreSQL + pgvector, and React.

## Features

- **Five-agent pipeline** orchestrated with LangGraph
- **RAG with pgvector**: web sources are chunked, embedded, stored, and retrieved by semantic similarity
- **Fact-checking**: each key claim gets a verdict (`supported`, `partially_supported`, `unsupported`), a confidence score, and its source numbers
- **Cited reports**: inline citations like `[1]`, `[2]` that match a numbered source list
- **Live progress**: the UI shows each agent as it runs (Server-Sent Events)
- **Session history**: every research run is saved; reopen, delete one, or clear all

## Why multiple agents?

Each agent has one job, which keeps prompts focused and results easier to inspect:

1. The fact checker works on retrieved evidence instead of the model's memory.
2. Structured claims let the pipeline drop unsupported statements before the report is written.
3. Intermediate outputs (sources, evidence, claims) are saved and visible, so the process is auditable.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                          USER INPUT                         │
│                     (Research question)                     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                        REACT FRONTEND                       │
│      (Query box, live agent progress, history sidebar)      │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     FASTAPI + LANGGRAPH                     │
│           (Sequential workflow with shared state)           │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                       AGENT 1: SEARCH                       │
│            Tavily web search, 6 numbered sources            │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   AGENT 2: RETRIEVAL (RAG)                  │
│     Chunk -> embed -> store in pgvector -> top 8 chunks     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    AGENT 3: FACT CHECKER                    │
│         Claims, verdict, confidence, source numbers         │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                       AGENT 4: ANALYST                      │
│        Findings, agreements, gaps (drops unsupported)       │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                  AGENT 5: REPORT GENERATOR                  │
│              Markdown report with [n] citations             │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                         FINAL OUTPUT                        │
│         (Report, fact-check table, numbered sources)        │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                  POSTGRES (NEON) + PGVECTOR                 │
│  (Saved sessions, evidence chunks, history: view / delete)  │
└─────────────────────────────────────────────────────────────┘
```

Evidence chunks and finished sessions (report, claims, sources) are stored in Postgres with pgvector, which powers the history sidebar.

| Agent | Responsibility |
|---|---|
| Search | Finds web sources for the query using Tavily |
| Retrieval | Chunks sources, embeds them, stores them in pgvector, returns the top matching chunks |
| Fact Checker | Extracts 5-8 key claims, verifies each against the evidence, scores confidence |
| Analyst | Synthesizes non-rejected claims into findings, agreements, and gaps |
| Report Generator | Writes a structured markdown report with inline citations |

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React (Vite), react-markdown |
| Backend | Python, FastAPI |
| Agent orchestration | LangGraph |
| LLM and embeddings | OpenRouter (OpenAI-compatible API) |
| Web search | Tavily |
| Database | PostgreSQL with pgvector (hosted on Neon) |
| ORM | SQLAlchemy |

## Project structure

```
ai-research-agent/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app, CORS, startup
│   │   ├── config.py            # Settings loaded from .env
│   │   ├── agents/              # The five agents
│   │   ├── graph/               # Shared state and LangGraph workflow
│   │   ├── services/            # LLM client and Tavily search
│   │   ├── database/            # Models and pgvector setup
│   │   └── api/                 # REST and streaming routes
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/          # UI components
│       ├── hooks/               # useResearch (streaming logic)
│       └── services/            # API helpers
└── README.md
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- A [Neon](https://neon.tech) Postgres database (free tier works, pgvector is supported)
- An [OpenRouter](https://openrouter.ai) API key
- A [Tavily](https://tavily.com) API key

## API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/research` | Run the full pipeline and return the report |
| GET | `/research/stream?query=...` | Same pipeline, streaming each agent's progress (SSE) |
| GET | `/sessions` | List saved sessions |
| GET | `/sessions/{id}` | Get one saved session |
| DELETE | `/sessions/{id}` | Delete one session and its stored chunks |
| DELETE | `/sessions` | Delete all sessions |


## Configuration

Models are set in `backend/app/config.py`:

- `llm_model` (default `openai/gpt-4o-mini`)
- `embedding_model` (default `openai/text-embedding-3-small`, 1536 dimensions)

If you change the embedding model to one with a different dimension, update `Vector(1536)` in `database/postgres.py` and recreate the `chunks` table.

## Limitations

- Report quality depends on the sources Tavily returns and on the LLM used.
- Citation accuracy is not automatically verified yet, so a citation can occasionally point to a loosely related source.
- No authentication or rate limiting. Do not expose a public deployment without adding them, since each query uses paid API credits.

## Roadmap

- [ ] Document RAG: PDF upload into the pgvector store
- [ ] Academic Search agent (arXiv / Semantic Scholar)
- [ ] Source Ranking: score sources by relevance and agreement
- [ ] Citation Manager: verify each citation against its source
- [ ] Evaluation script (query set, citation validity, claim support rate)
- [ ] Docker and docker-compose setup
- [ ] PDF export of the report
- [ ] Retries and timeouts for agents
- [ ] Deployment (Render for backend, Vercel for frontend)
