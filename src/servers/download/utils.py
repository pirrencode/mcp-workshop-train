from functools import reduce
from html2text import HTML2Text

def get_text2html() -> HTML2Text:
    result = HTML2Text()
    result.ignore_links = False
    result.ignore_images = False
    result.ignore_tables = False
    result.body_width = 0
    return result

def flatten(xss):
    return reduce(lambda xs, ys: xs + ys, xss)
