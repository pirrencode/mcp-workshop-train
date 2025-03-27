import logging
from os import environ, path, getenv
from dotenv import load_dotenv

def find_up(expected: str , initial:str =__file__):
    abs_file = path.join(path.abspath(initial), expected)
    if path.exists(abs_file):
        return abs_file
    parent_dir = path.dirname(initial)
    if parent_dir == initial:
        return None
    return find_up(expected, parent_dir)

SRC_DIR_ABS = find_up("src")
DOT_ENV_ABSPATH = find_up(".env")

load_dotenv(DOT_ENV_ABSPATH)

LOG_LEVEL = environ.setdefault("LOG_LEVEL", "INFO").upper()

FASTMCP_DEFAULTS = {
    "log_level":    LOG_LEVEL,
    "debug":        getattr(logging, getenv("LOG_LEVEL"), logging.INFO) <= logging.DEBUG,
}

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

