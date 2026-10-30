from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from app.config import settings

llm = ChatOpenAI(
    model=settings.llm_model,
    api_key=settings.openrouter_api_key,
    base_url=settings.openrouter_base_url,
    temperature=0,
)

embedder = OpenAIEmbeddings(
    model=settings.embedding_model,
    api_key=settings.openrouter_api_key,
    base_url=settings.openrouter_base_url,
    check_embedding_ctx_length=False,
)