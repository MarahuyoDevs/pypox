from pypox.processor.base import BaseProcessor, Response, WebSocket, Any, Request


class WebSocketProcessor(BaseProcessor):
    """
    A processor that handles WebSocket connections.
    """

    def __init__(self, response_class: type[Response] | None = None):
        super().__init__([WebSocket], response_class)

    async def encode(
        self, request: WebSocket, name: str, annotation: type
    ) -> dict[str, Any] | None:
        """Encodes the request data.

        Args:
            request (WebSocket): The WebSocket object representing the request.
            name (str): The name of the request.
            annotation (type): The type annotation of the request.

        Returns:
            dict[str, Any] | None: The encoded data as a dictionary, or None if the annotation is not supported.
        """
        if annotation in self.types:
            return {name: request}

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
