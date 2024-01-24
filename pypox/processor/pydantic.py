from pypox.processor.base import BaseProcessor, Request, Response, JSONResponse, Any

try:
    from pydantic import BaseModel
except ImportError as exc:
    raise exc


class PydanticProcessor(BaseProcessor):
    """
    A processor that handles Pydantic models in a request.
    """

    def __init__(
        self,
        response_class: type[Response] | None = JSONResponse,
    ):
        super().__init__([BaseModel], response_class)

    async def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        """Encode the request data based on the provided annotation.

        Args:
            request (Request): The request object containing the data to be encoded.
            name (str): The name of the data field.
            annotation (type): The type annotation of the data field.

        Returns:
            dict[str, Any] | None:
            The encoded data as a dictionary, or None if the annotation is not a subclass of BaseModel.
        """
        if issubclass(annotation, BaseModel):
            return {name: annotation(**(await request.json()))}
        return None

    async def decode(self, request: Request, response: Any) -> Response | None:
        """Decodes the response object.

        Args:
            request (Request): The request object.
            response (Any): The response object.

        Returns:
            Response | None: The decoded response object, or None if decoding is not applicable.
        """
        if issubclass(type(response), BaseModel) and self.response_class:
            return self.response_class(content=response.model_dump())

    async def exception(self, request: Request, exception: Exception):
        """Handles exceptions that occur during request processing.

        Args:
            request (Request): The request object.
            exception (Exception): The exception that occurred.

        Returns:
            The response to be sent back to the client.
        """
        return await super().exception(request, exception)
