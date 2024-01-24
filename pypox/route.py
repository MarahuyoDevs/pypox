from inspect import iscoroutinefunction
from typing import Any
from inspect import iscoroutinefunction
from typing import Any
from functools import wraps
from starlette.responses import (
    Response,
    JSONResponse,
    HTMLResponse,
    RedirectResponse,
    PlainTextResponse,
    StreamingResponse,
    FileResponse,
)


class RouteInfo:
    """
    A class representing the information about a route.

    Attributes:
        status_code (int): The status code of the route.
        response (Any): The response of the route.

    """

    def __init__(self, status_code: int, response: Any) -> None:
        self._status_code = status_code
        self._response = response

    @property
    def status_code(self) -> int:
        """
        Returns the status code.

        Returns:
            int: The status code.
        """
        return self._status_code

    @property
    def response(self) -> Any:
        """
            return the response data
        Returns:
            Any: The response data.
        """
        return self._response


def route(status_code: int = 200) -> Any:
    def decorator(func) -> Any:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if iscoroutinefunction(func):
                response = await func(*args, **kwargs)
            else:
                response = func(*args, **kwargs)
            if type(response) in [
                Response,
                JSONResponse,
                HTMLResponse,
                RedirectResponse,
                PlainTextResponse,
                StreamingResponse,
                FileResponse,
            ]:
                return response
            return RouteInfo(status_code, response)

        return wrapper

    return decorator
