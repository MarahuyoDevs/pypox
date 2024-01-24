from pypox.processor.base import BaseProcessor, Response, JSONResponse, Request, Any


class JSONProcessor(BaseProcessor):
    """
    A processor for handling JSON data.

    This processor is responsible for encoding and decoding JSON data.

    Args:
        BaseProcessor (type): The base processor class.

    Attributes:
        types (list[type]): A list of types that can be encoded/decoded.
        response_class (type[Response] | None): The response class to use for decoding.
    """

    def __init__(
        self,
        types: list[type] | None = None,
        response_class: type[Response] | None = JSONResponse,
    ) -> None:
        if not types:
            types = []
        super().__init__([list, dict] + types, response_class)

    async def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        """Encode the request data.

        Args:
            request (Request): The request object.
            name (str): The name of the data.
            annotation (type): The type annotation of the data.

        Returns:
            dict[str, Any] | None: The encoded data or None if encoding is not possible.

        """
        if annotation in self.types:
            return {name: annotation(await request.json())}
        return None

    async def decode(self, request: Request, response: Any) -> Response | None:
        """Decode the response data.

        Args:
            request (Request): The request object.
            response (Any): The response data.

        Returns:
            Response | None: The decoded response or None if decoding is not possible.

        """
        if type(response) in self.types:
            if self.response_class:
                return self.response_class(content=response)
        return None

    async def exception(self, request: Request, exception: Exception):
        """Handles exceptions that occur during request processing.

        Args:
            request (Request): The request object.
            exception (Exception): The exception that occurred.

        Returns:
            The response to be sent back to the client.
        """
        return await super().exception(request, exception)
