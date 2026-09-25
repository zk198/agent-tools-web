import asyncio
from agent_tools_web.mcp import mcp

def test_mcp_projection_is_explicit():
    names = {tool.name for tool in asyncio.run(mcp.list_tools())}
    assert names == {"web_search", "fetch_url"}
