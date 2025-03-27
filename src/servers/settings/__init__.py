from mcp.server.fastmcp.utilities.logging import configure_logging, get_logger

from .main import (
    FASTMCP_DEFAULTS,
    DOT_ENV_ABSPATH,
    DEFAULT_HEADERS,
    LOG_LEVEL,
    find_up,
)

configure_logging(LOG_LEVEL)
logger = get_logger(name=__name__)
