from math import e
import os
from threading import Thread
from types import ModuleType
from typing import Any, Generator, Union
import aiofiles
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException, Request, Response
from jinja2 import Environment, FileSystemLoader, Template
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import HTTPException
from starlette.exceptions import HTTPException
import importlib.util
import asyncio

VANGUARD_CONVENTIONS: list[str] = [
    "layout.html",
    "page.html",
    "script.py",
    "load.py",
    "404.html",
]

VanguardRoutes = dict[str, dict[str, Union[ModuleType, Template, str, Any]]]


class VanguardMiddleware(BaseHTTPMiddleware):
    base_template: Template
    error_template: Template

    def __init__(
        self,
        app,
        route_dir: str = "routes",
        static_dir: str = "static",
        pyodide_dir: str = "pyodide",
        enable_pyodide: bool = True,
        base_html: str = "index.html",
        error_html: str = "error.html",
    ) -> None:
        super().__init__(app)

        self.routes: VanguardRoutes = {}

        async def _init_async():
            self.base_template = await self.loadTemplate(base_html, static_dir)
            self.error_template = await self.loadTemplate(error_html, static_dir)
            for root, convention, route in self.walk(route_dir):
                if convention in [x for x in VANGUARD_CONVENTIONS if ".py" in x]:
                    module: ModuleType | str = await self.loadPython(convention, root)
                    if module:
                        self.routes.setdefault(route, {}).update({convention: module})
                if convention in [x for x in VANGUARD_CONVENTIONS if ".html" in x]:
                    template: Template = await self.loadTemplate(convention, root)
                    if template:
                        self.routes.setdefault(route, {}).update({convention: template})

        # run the async function in a separate thread
        try:
            _init_thread = Thread(target=asyncio.run, args=(_init_async(),))
            _init_thread.start()
            _init_thread.join()
        except Exception as e:
            raise e

    async def loadPython(self, name: str, directory: str) -> ModuleType | str:
        if not os.path.exists(directory + f"/{name}"):
            raise OSError(
                f"Python file '{name}' does not exist in directory '{directory}'"
            )

        if name == "script.py":
            async with aiofiles.open(directory + f"/{name}", mode="r") as f:
                return await f.read()

        spec = importlib.util.spec_from_file_location(name, directory + f"/{name}")
        module = importlib.util.module_from_spec(spec)  # type: ignore
        try:
            spec.loader.exec_module(module)  # type: ignore
        except Exception as e:
            raise OSError(
                f"Error loading module '{name}' in directory '{directory}'"
            ) from e
        return module

    async def loadTemplate(self, name: str, directory: str) -> Template:
        if not os.path.exists(directory + f"/{name}"):
            raise OSError(
                f"Template file '{name}' does not exist in directory '{directory}'"
            )
        template = Environment(
            loader=FileSystemLoader(directory),
        ).get_template(name)
        return template

    def walk(self, directory: str) -> Generator[tuple[str, str, str], Any, None]:
        for root, _, files in os.walk(directory):
            for convention in VANGUARD_CONVENTIONS:
                if convention in files:
                    root = root.rstrip("/") + "/"
                    if root == "/":
                        yield root, convention, root
                    else:
                        yield root, convention, root.replace(directory, "").replace(
                            "\\", "/"
                        ).replace("[", "{").replace("]", "}").replace("\\routes\\", "/")

    async def dispatch(
        self, request: Request, call_next
    ) -> HTMLResponse | JSONResponse | Response | None:
        try:
            url_path = (
                request.url.path + "/"
                if not request.url.path.endswith("/")
                else request.url.path
            )
            if url_path in self.routes:
                if (
                    request.headers.get("X-Requested-With") == "XMLHttpRequest"
                    and request.headers.get("Content-Type") == "application/python"
                ):
                    return await self.renderHTML(request, "partial")
                else:
                    if "text/html" in request.headers.get("accept", "").split(","):
                        return await self.renderHTML(request, "full")
                if url_path not in self.routes:
                    raise HTTPException(detail="Page Not Found", status_code=404)
            else:
                return await call_next(request)
        except HTTPException as e:
            return HTMLResponse(
                content=self.base_template.render(
                    request=request, error_message=e.detail, error_code=e.status_code
                ),
                status_code=e.status_code,
            )

    async def render(
        self, url_path: str, request: Request, mode: str = "full"
    ) -> Union[HTMLResponse, JSONResponse]:
        loaded_data: dict = {"head": ""}

        if "load.py" in self.routes[url_path]:
            loaded_data.update(
                await self.routes[url_path]["load.py"].load(request)  # type: ignore
            )
        html = (
            self.routes[url_path]["page.html"].render(**loaded_data)  # type: ignore
            if loaded_data
            else self.routes[url_path]["page.html"].render()  # type: ignore
        )

        rendered_layouts = set()
        current_route = ""
        for route in url_path.split("/")[:-1][::-1]:
            if not route:
                route = "/"
            if not current_route:
                current_route = url_path
            # get first the route layout before getting other layouts
            if current_route == url_path:
                # get the layout page
                if "layout.html" in self.routes[url_path]:
                    html = self.routes[url_path]["layout.html"].render(  # type: ignore
                        slot=html, **loaded_data
                    )
                    rendered_layouts.add(url_path)

            current_route = current_route.replace(route + "/", "")

            if current_route not in rendered_layouts:
                if "layout.html" in self.routes[current_route]:
                    html = self.routes[current_route]["layout.html"].render(  # type: ignore
                        slot=html, **loaded_data
                    )
                    rendered_layouts.add(current_route)
        if "script.py" in self.routes[url_path]:
            if mode == "full":
                return HTMLResponse(
                    content=self.base_template.render(
                        slot=html,
                        script=self.routes[url_path]["script.py"] or "",
                        **loaded_data,
                    ),
                    status_code=200,
                )
            else:
                return JSONResponse(
                    content={
                        "body": html,
                        "script": self.routes[url_path]["script.py"] or "",
                        **loaded_data,
                    }
                )
        else:
            if mode == "full":
                return HTMLResponse(
                    content=self.base_template.render(
                        slot=html,
                        **loaded_data,
                    ),
                    status_code=200,
                )
            else:
                return JSONResponse(
                    content={
                        "body": html,
                        **loaded_data,
                    }
                )

    async def renderHTML(
        self, request: Request, mode: str
    ) -> HTMLResponse | JSONResponse:
        url_path = (
            request.url.path + "/"
            if request.url.path != "/" and request.url.path[-1] != "/"
            else request.url.path
        )
        try:
            if "page.html" not in self.routes[url_path]:
                raise HTTPException(status_code=404)
            return await self.render(url_path, request, mode)
        except HTTPException as e:
            error_template = self.routes[url_path].get("404.html")
            if not error_template:
                error_template = self.error_template
            return HTMLResponse(
                content=error_template.render(request=request, error_message=e.detail),  # type: ignore
                status_code=404,
            )
