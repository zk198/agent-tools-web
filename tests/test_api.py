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


def test_fetch_rejects_private_destination():
    response = client.post("/v1/fetch", json={"url": "http://127.0.0.1/"})
    assert response.status_code == 400


def test_public_resolver_rejects_private_address(monkeypatch):
    import asyncio
    import socket
    import pytest
    from agent_tools_web.service import PublicResolver
    monkeypatch.setattr(socket, "getaddrinfo", lambda *args: [(socket.AF_INET, 0, 0, "", ("127.0.0.1", 80))])
    with pytest.raises(ValueError, match="public"):
        asyncio.run(PublicResolver().resolve("example.test", 80))
