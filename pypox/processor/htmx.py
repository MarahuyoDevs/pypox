from typing import Mapping
from pypox.processor.base import BaseProcessor, Response, HTMLResponse, Request, Any
from starlette.background import BackgroundTask
try:
    from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound
except ImportError as exc:
    raise exc


class HTMXProcessor(BaseProcessor):
    """
    A processor that renders HTMX templates.
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
        if not isinstance(response, HTMXResponse):
            return None

        if not isinstance(response.content, dict) or isinstance(response.content, str):
            if self.response_class:
                return self.response_class(
                    content=response.content,
                    status_code=response.status_code,
                    headers=response.headers,
                    media_type=response.media_type,
                    background=response.background,
                )

        page: str = await self.environment.get_template(
            request.url.path + self.convention["page"]
        ).render_async(**response.content)

        routes: list[str] = [x for x in request.url.path.split("/") if x]

        html: str = ""

        for index in reversed(range(len(routes))):
            if not index:
                path = "/" + "/".join(routes[:-1] + [routes[-1]]) + "/"
            else:
                path = "/" + "/".join(routes[:-index]) + "/"
            try:
                print(path)
                layout: Template = self.environment.get_template(
                    path + self.convention["layout"]
                )
                if not html:
                    html = await layout.render_async(slot=page)
                if html:
                    html = await layout.render_async(slot=html)
            except TemplateNotFound:
                continue
        try:
            if not html:
                html = await self.environment.get_template(
                    self.convention["layout"]
                ).render_async(slot=page)
        except TemplateNotFound:
            html = page

        if self.response_class:
            return self.response_class(
                content=html,
                status_code=response.status_code,
                headers=response.headers,
                media_type=response.media_type,
                background=response.background,
            )

        return None

    async def exception(self, request: Request, exception: Exception):
        return await super().exception(request, exception)


class HTMXResponse:
    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        self.content = content
        self.status_code = status_code
        self.headers = headers
        self.media_type = media_type
        self.background = background
