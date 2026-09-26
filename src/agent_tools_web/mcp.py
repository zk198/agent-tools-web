from fastmcp import FastMCP
from fastmcp.server.providers.openapi import MCPType, RouteMap
from .api import app

# Explicit allow-list: only routes tagged "llm" are exposed.
# Catch-all EXCLUDE prevents future REST endpoints becoming MCP tools accidentally.
mcp = FastMCP.from_fastapi(
    app=app,
    name="Agent Web Tools",
    route_maps=[
        RouteMap(tags={"llm"}, mcp_type=MCPType.TOOL),
        RouteMap(mcp_type=MCPType.EXCLUDE),
    ],
)
mcp_app = mcp.http_app(path="/mcp", stateless_http=True)
