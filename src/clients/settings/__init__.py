from os.path import dirname
from os import getenv

from servers.settings import (
    LOG_LEVEL,
    DOT_ENV_ABSPATH,
    DEFAULT_HEADERS,
    configure_logging,
    get_logger,
    find_up,
)

PROJECT_ROOT    = dirname(find_up("pyproject.toml"))
PROJECT_SRC     = find_up("src")
PYTHONPATH      = f"{PROJECT_SRC}:{PROJECT_ROOT}"
SLACK_APP_TOKEN = getenv("SLACK_APP_TOKEN")
SLACK_BOT_TOKEN = getenv("SLACK_BOT_TOKEN")

configure_logging(LOG_LEVEL)
logger = get_logger(name=__name__)
