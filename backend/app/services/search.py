from tavily import TavilyClient
from app.config import settings

_client = TavilyClient(api_key=settings.tavily_api_key)

def web_search(query: str, max_results: int = 6) -> list[dict]:
    results = _client.search(query, max_results=max_results, search_depth="advanced")
    return [
        {
            "index": i + 1,
            "title": r["title"],
            "url": r["url"],
            "content": r["content"],
        }
        for i, r in enumerate(results["results"])
    ]