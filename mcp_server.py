"""
Your MCP server. ← UNIT 4, MILESTONE 1

This server exposes one FitFindr tool through MCP:
search_listings.

The underlying search logic still lives in tools.py.
This file only registers that tool so an MCP client can call it.
"""

from mcp.server.fastmcp import FastMCP

from tools import search_listings as _search_listings_impl


# Keep MCP logging quiet so useful output is easier to read.
mcp = FastMCP(
    "fitfindr",
    log_level="WARNING",
)


# ── MCP Tool: search_listings ─────────────────────────────────────────────────

@mcp.tool()
def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search thrift listings using a text description, optional size, and optional
    maximum price in dollars.

    Returns matching listing dictionaries ranked by relevance.
    Returns an empty list when no listings match.
    """

    return _search_listings_impl(
        description,
        size,
        max_price,
    )


if __name__ == "__main__":
    mcp.run()