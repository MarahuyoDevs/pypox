from pypox.processor.base import BaseProcessor, Response, Request, Any


class HeaderProcessor(BaseProcessor):
    """
    A processor that handles headers in a request.
    """

    def __init__(self, response_class: type[Response] | None = None):
        super().__init__([str], response_class)

    async def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        """Encode the request header value based on the given annotation.

        Args:
            request (Request): The request object.
            name (str): The name of the header.
            annotation (type): The type annotation for the header value.

        Returns:
            dict[str, Any] | None: A dictionary containing the encoded header value,
                or None if the annotation or header is not found.
        """
        if annotation in self.types and name in request.headers:
            return {name.replace("-", "_"): annotation(request.headers[name])}
        return None

    async def decode(self, request: Request, response: Any) -> Response | None:
        """
        Decodes the response data based on the provided annotation.

        Args:
            request (Request): The request object.
            response (Any): The response data.

        Returns:
            Response | None: A response class that can be used by the starlette app.
        """
        return await super().decode(request, response)

    async def exception(self, request: Request, exception: Exception):
        """Handles exceptions that occur during request processing.

        Args:
            request (Request): The request object.
            exception (Exception): The exception that occurred.

        Returns:
            The response to be sent back to the client.
        """
        return await super().exception(request, exception)
