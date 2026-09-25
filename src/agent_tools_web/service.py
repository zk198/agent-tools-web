from urllib.parse import urlparse
import httpx
from .models import FetchResponse, SearchResponse, SearchResult

class WebService:
    def __init__(self, timeout: float = 15.0, max_bytes: int = 1_000_000) -> None:
        self.timeout = timeout
        self.max_bytes = max_bytes

    async def search(self, query: str, limit: int) -> SearchResponse:
        return SearchResponse(results=[
            SearchResult(title=f"Search result for: {query}", url="https://example.invalid/",
                snippet="Search provider not configured.",)
        ][:limit])

    async def fetch(self, url: str) -> FetchResponse:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Only absolute HTTP(S) URLs are allowed")
        async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=False) as client:
            response = await client.get(url)
            response.raise_for_status()
            raw = response.content[: self.max_bytes + 1]
        truncated = len(raw) > self.max_bytes
        content = raw[: self.max_bytes].decode(response.encoding or "utf-8", errors="replace")
        return FetchResponse(url=str(response.url), content=content, truncated=truncated)
