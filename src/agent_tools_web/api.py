from fastapi import APIRouter, FastAPI, HTTPException
import httpx

from .models import FetchRequest, FetchResponse, SearchRequest, SearchResponse
from .service import WebService

service = WebService()
app = FastAPI(title="Agent Tools Web", version="0.2.0")
router = APIRouter(prefix="/v1")


@router.post("/search", response_model=SearchResponse, operation_id="web_search", tags=["llm"])
async def search(request: SearchRequest) -> SearchResponse:
    try:
        return await service.search(request.query, request.limit)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except (ValueError, httpx.HTTPError) as exc:
        raise HTTPException(status_code=502, detail="search provider failed") from exc


@router.post("/fetch", response_model=FetchResponse, operation_id="fetch_url", tags=["llm"])
async def fetch(request: FetchRequest) -> FetchResponse:
    try:
        return await service.fetch(request.url)
    except (ValueError, httpx.HTTPError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/health", tags=["internal"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(router)
