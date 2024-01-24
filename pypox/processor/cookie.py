from pypox.processor.base import BaseProcessor, Request, Response, Any


class CookieProcessor(BaseProcessor):
    """A processor for encoding and decoding cookies.

    This processor is responsible for encoding and decoding cookies in HTTP requests.

    Args:
        BaseProcessor (type): The base processor class.

    """

    def __init__(self, response_class: type[Response] | None = None):
        super().__init__([str], response_class)

    async def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        if annotation in self.types and name in request.cookies:
            return {name: annotation(request.cookies[name])}
        return None

    async def decode(self, request: Request, response: Any) -> Response | None:
        return await super().decode(request, response)

    async def exception(self, request: Request, exception: Exception):
        return await super().exception(request, exception)
