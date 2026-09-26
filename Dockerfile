FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.10.0 /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock* ./
RUN uv sync --locked --no-dev --no-install-project
COPY src ./src
RUN uv sync --locked --no-dev
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000 8001
CMD ["sh", "-c", "uvicorn agent_tools_web.api:app --host 0.0.0.0 --port 8000 & API=$!; fastmcp run src/agent_tools_web/mcp.py:mcp --transport http --host 0.0.0.0 --port 8001 & MCP=$!; while kill -0 $API 2>/dev/null && kill -0 $MCP 2>/dev/null; do sleep 1; done; kill $API $MCP 2>/dev/null || true; wait $API $MCP 2>/dev/null || true"]
