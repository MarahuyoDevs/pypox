from pypox.processor.base import BaseProcessor, Response, Request, HTMLResponse, Any

try:
    from jinja2 import Environment, FileSystemLoader, Template
except ImportError as exc:
    raise exc


class JinjaProcessor(BaseProcessor):
    """
    A processor that renders Jinja templates.
    """

    def __init__(
        self, template_dir: str, response_class: type[Response] | None = HTMLResponse
    ):
        super().__init__([], response_class)
        self.environment = Environment(
            loader=FileSystemLoader(template_dir),
            line_statement_prefix="#",
            line_comment_prefix="##",
            enable_async=True,
        )
        self.convention: dict = {
            "page": "page.html",
            "layout": "layout.html",
            "error": "error.html",
        }

    async def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        return await super().encode(request, name, annotation)

    async def decode(self, request: Request, response: Any):
        """Decodes the request and generates a response.

        Args:
            request (Request): The request object.
            response (Any): The response object.

        Returns:
            The generated response object.
        """
        if "text/html" in request.headers.get("accept", "").split(","):
            page: Template = self.environment.get_template(
                request.url.path + self.convention["page"]
            )
            if self.response_class:
                return self.response_class(content=page.render(**self.convention))
        return None

    async def exception(self, request: Request, exception: Exception):
        return await super().exception(request, exception)
