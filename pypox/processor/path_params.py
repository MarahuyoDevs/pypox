from pypox.processor.base import BaseProcessor, Response, Request, Any


class PathProcessor(BaseProcessor):
    """
    A processor that extracts and encodes path parameters from a request.
    """
    def __init__(
        self,
        types: list[type] | None = None,
        response_class: type[Response] | None = None,
    ):
        if not types:
            types = []
        super().__init__([int, float, str, bool] + types, response_class)

    async def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        if annotation in self.types and name in request.path_params:
            return {name: annotation(request.path_params[name])}
        return None

    async def decode(self, request: Request, response: Any) -> Response | None:
        return await super().decode(request, response)

    async def exception(self, request: Request, exception: Exception):
        return await super().exception(request, exception)
