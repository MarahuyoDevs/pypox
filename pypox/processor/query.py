from pypox.processor.base import BaseProcessor, Request, Response, Any


class QueryProcessor(BaseProcessor):
    """
    Processor class for handling query parameters in requests.
    """

    def __init__(
        self,
        types: list[type] | None = None,
        response_class: type[Response] | None = None,
    ):
        if types is None:
            types = []
        super().__init__(types + [int, float, str, bool], response_class)

    async def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        """
        Encodes the query parameter value based on the provided annotation.

        Args:
            request (Request): The request object.
            name (str): The name of the query parameter.
            annotation (type): The type annotation of the query parameter.

        Returns:
            dict[str, Any] | None:
        """
        if annotation in self.types and name in request.query_params:
            return {name: annotation(request.query_params[name])}
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
