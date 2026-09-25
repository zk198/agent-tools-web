from fastapi.testclient import TestClient
from agent_tools_web.api import app

client = TestClient(app)

def test_health():
    assert client.get("/health").json() == {"status": "ok"}

def test_search_contract():
    response = client.post("/v1/search", json={"query": "python", "limit": 2})
    assert response.status_code == 200
    assert "results" in response.json()

def test_mcp_allowlist():
    import asyncio
    from agent_tools_web.mcp import mcp
    names = {tool.name for tool in asyncio.run(mcp.list_tools())}
    assert {"web_search", "fetch_url"} <= names
    assert "health" not in names
