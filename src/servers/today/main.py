#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict
import datetime
from mcp.server.fastmcp import FastMCP
from servers.settings import logger, FASTMCP_DEFAULTS

mcp = FastMCP("Today", settings=FASTMCP_DEFAULTS)

@mcp.tool()
def today() -> Dict[str, str]:
    """
    Get current date, time, and calendar information.

    Use this tool when you need to know:
    - The current date and time
    - What day of the week it is
    - The current year, month, or day
    - Timestamp information for calculations

    Returns:
        A dictionary containing these date and time components:
        - date: Current date in YYYY-MM-DD format (e.g., "2025-03-26")
        - full_date: Formatted date with day of week (e.g., "Wednesday, March 26, 2025")
        - weekday: Current day of the week (e.g., "Wednesday")
        - year: Current year (e.g., "2025")
        - month: Current month name (e.g., "March")
        - day: Day of month (e.g., "26")
        - time: Current time in 24-hour format (e.g., "14:30:22")
        - iso_format: ISO 8601 formatted datetime (e.g., "2025-03-26T14:30:22.123456")
        - timestamp: Unix timestamp as seconds since epoch (e.g., 1742862622)
    """
    today = datetime.datetime.now()
    return {
        "date": today.strftime("%Y-%m-%d"),
        "full_date": today.strftime("%A, %B %d, %Y"),
        "weekday": today.strftime("%A"),
        "year": today.strftime("%Y"),
        "month": today.strftime("%B"),
        "day": today.strftime("%d"),
        "time": today.strftime("%H:%M:%S"),
        "iso_format": today.isoformat(),
        "timestamp": int(today.timestamp())
    }

if __name__ == "__main__":
    logger.info(f"Starting MCP server: {mcp.name}...")
    mcp.run(transport="stdio")
