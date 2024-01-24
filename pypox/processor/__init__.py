"""
    This module contains the processors used by the pypox framework.

    The processors handle different aspects of the HTTP request and response, such as cookies, headers, JSON data,
    path parameters, query parameters, and websockets.

    Optional dependencies include PydanticProcessor, HTMXProcessor, and JinjaProcessor.
"""

from pypox.processor.cookie import CookieProcessor
from pypox.processor.header import HeaderProcessor
from pypox.processor.json import JSONProcessor
from pypox.processor.path_params import PathProcessor
from pypox.processor.query import QueryProcessor
from pypox.processor.websocket import WebSocketProcessor

try:
    # Optional dependencies
    from pypox.processor.pydantic import PydanticProcessor
    from pypox.processor.htmx import HTMXProcessor
    from pypox.processor.jinja import JinjaProcessor
except ImportError:
    pass
