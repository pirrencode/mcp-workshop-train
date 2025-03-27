#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httpx
from typing import List, Dict
from os import getenv

from mcp.server.fastmcp import FastMCP
from servers.settings import FASTMCP_DEFAULTS, DEFAULT_HEADERS, logger

GOOGLE_SEARCH_CREDS = {
    "key": getenv("GOOGLE_API_KEY"),
    "cx":  getenv("GOOGLE_ENGINE_ID"),
}

fastmcp_settings = {
    **FASTMCP_DEFAULTS,
    "dependencies": ["httpx"]
}
mcp = FastMCP("DownloadPage", settings=fastmcp_settings)

@mcp.tool()
def google_search(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Search the web for current information, news, and facts using Google.

    Use this tool when you need to find:
    - Current events or recent information not in your training data
    - Up-to-date facts, prices, or statistics
    - Specific information that you're uncertain about

    Parameters:
        query: The specific search terms or question to look up online
        num_results: Number of results to return (1-10, default: 5)

    Returns:
        A list of search results, each containing:
        - title: The title of the webpage
        - link: The URL to the full webpage
        - snippet: A brief text extract from the webpage showing relevant content

    Example return value:
    [
        {
            "title": "Latest Climate Report - Example.com",
            "link": "https://example.com/climate-report",
            "snippet": "The 2025 climate assessment shows global temperatures have risen by..."
        },
        ...
    ]
    """

    logger.info(f"Searching online for: {query}")
    with httpx.Client(timeout=10.0) as client:
        response = client.get(
            url="https://www.googleapis.com/customsearch/v1",
            params={
                **GOOGLE_SEARCH_CREDS,
                "q": query,
                "num": min(num_results, 10),
            },
            headers=DEFAULT_HEADERS,
            )
        response.raise_for_status()
        search_results = response.json()

    results = [
        {
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "snippet": item.get("snippet", "")
        }
        for item in search_results.get("items", [])
    ]
    logger.info(f"Got {len(results)} in response")
    return results


if __name__ == "__main__":
    logger.info(f"Starting MCP server: {mcp.name}...")
    mcp.run(transport="stdio")
