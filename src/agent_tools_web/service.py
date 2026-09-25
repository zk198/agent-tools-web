import asyncio
import ipaddress
import socket
from urllib.parse import urlparse

import aiohttp

from .models import FetchResponse, SearchResponse, SearchResult

class PublicResolver(aiohttp.abc.AbstractResolver):
    async def resolve(self, host: str, port: int = 0, family: int = socket.AF_UNSPEC):
        infos = await asyncio.to_thread(socket.getaddrinfo, host, port, family, socket.SOCK_STREAM)
        addresses = []
        for _, _, _, _, sockaddr in infos:
            address = sockaddr[0]
            ip = ipaddress.ip_address(address)
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
                continue
            addresses.append({
                "hostname": host,
                "host": address,
                "port": port,
                "family": family or socket.AF_INET,
                "proto": 0,
                "flags": 0,
            })
        if not addresses:
            raise ValueError("Destination address is not public")
        return addresses

    async def close(self) -> None:
        return None

class WebService:
    def __init__(self, timeout: float = 15.0, max_bytes: int = 1_000_000) -> None:
        self.timeout = timeout
        self.max_bytes = max_bytes

    async def search(self, query: str, limit: int) -> SearchResponse:
        return SearchResponse(results=[
            SearchResult(title=f"Search result for: {query}", url="https://example.invalid/",
                         snippet="Search provider not configured.")
        ][:limit])

    async def fetch(self, url: str) -> FetchResponse:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("Only absolute HTTP(S) URLs are allowed")
        try:
            literal = ipaddress.ip_address(parsed.hostname)
        except ValueError:
            literal = None
        if literal is not None and (
            literal.is_private or literal.is_loopback or literal.is_link_local
            or literal.is_reserved or literal.is_multicast
        ):
            raise ValueError("Destination address is not public")
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        connector = aiohttp.TCPConnector(resolver=PublicResolver(), use_dns_cache=False)
        async with aiohttp.ClientSession(timeout=timeout, connector=connector, trust_env=False) as client:
            async with client.get(url, allow_redirects=False) as response:
                response.raise_for_status()
                raw = await response.content.read(self.max_bytes + 1)
                truncated = len(raw) > self.max_bytes
                content = raw[:self.max_bytes].decode(response.charset or "utf-8", errors="replace")
                return FetchResponse(url=str(response.url), content=content, truncated=truncated)
