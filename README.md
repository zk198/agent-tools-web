# Agent Tools Web

REST and Streamable HTTP MCP web capabilities.

## Search provider

Search is delegated to a configurable SearXNG-compatible JSON endpoint via
`WEB_SEARCH_URL`. SearXNG is the default local Compose provider; the service
expects `/search?q=...&format=json` and maps its `results` array into the
stable tool contract.

The `fetch` tool rejects private, loopback, link-local, reserved and multicast
destination addresses and does not follow redirects. Redirects are deliberately
left to the caller so the destination is revalidated before another fetch.
