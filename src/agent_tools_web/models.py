from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    limit: int = Field(default=5, ge=1, le=10)

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str

class SearchResponse(BaseModel):
    results: list[SearchResult]

class FetchRequest(BaseModel):
    url: str = Field(min_length=8, max_length=2048)

class FetchResponse(BaseModel):
    url: str
    content: str
    truncated: bool
