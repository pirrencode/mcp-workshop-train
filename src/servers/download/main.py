#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httpx
from bs4 import BeautifulSoup

from mcp.server.fastmcp import FastMCP
from servers.settings import FASTMCP_DEFAULTS, DEFAULT_HEADERS, logger
from servers.download.utils import get_text2html

UNWANTED_HTML_TAGS = ["script", "style", "nav", "footer", "iframe", "noscript"]

h2t = get_text2html()

fastmcp_settings = {
    **FASTMCP_DEFAULTS,
    "dependencies": ["bs4", "text2html"],
}
mcp = FastMCP("OnlineSearch", settings=fastmcp_settings)

@mcp.tool()
def download_webpage(url: str, extract_main_content: bool = True, timeout: int = 15) -> str:
    """
    Download and extract content from a webpage, converting it to formatted Markdown text.

    Use this tool when you need to:
    - Get detailed information from a specific webpage
    - Read article content from news sites, blogs, or documentation
    - Analyze text from a URL that was mentioned in conversation

    Parameters:
        url: The complete URL of the webpage to download (must include http:// or https://)
        extract_main_content: If True, attempts to find and extract only the main article content
                             If False, returns the entire webpage content
        timeout: Maximum time in seconds to wait for the webpage to load (default: 15)

    Returns:
        A Markdown-formatted string containing:
        1. The webpage title as a heading
        2. The source URL
        3. The extracted content with formatting preserved

    Example return value:
    ```
    # Example Article Title

    Source: https://example.com/article

    This is the main content of the article with **formatting** preserved.

    - List items
    - Are maintained

    As are paragraph breaks and [links](https://example.com).
    ```
    """
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        response = client.get(url, headers=DEFAULT_HEADERS)
        response.raise_for_status()

    bs = BeautifulSoup(response.text, 'html.parser')
    title_tag = bs.find('title')
    title = title_tag.text.strip() if title_tag else ""
    for element in bs(UNWANTED_HTML_TAGS):
        element.extract()

    content_html = None
    if extract_main_content:
        main_content = None
        for selector in ['main', 'article', '[role="main"]', '#main-content', '.main-content', '#content', '.content', '.post', '.entry']:
            main_content = bs.select_one(selector)
            if main_content:
                break

        if main_content:
            content_html = str(main_content)
        else:
            divs = bs.find_all('div')
            if divs:
                main_content = max(divs, key=lambda d: len(d.find_all('p')))
                content_html = str(main_content)

    if not content_html:
        body = bs.find('body')
        content_html = str(body) if body else str(bs)

    markdown_content = h2t.handle(content_html)
    result = ""
    if title:
        result += f"# {title}\n\n"
    result += f"Source: {url}\n\n"
    result += markdown_content
    logger.info("Downloaded document")
    logger.info(result)
    return result

if __name__ == "__main__":
    logger.info(f"Starting MCP server: {mcp.name}...")
    mcp.run(transport="stdio") # or "sse"
