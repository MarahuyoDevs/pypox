from pypox.application import PypoxHTMX
from pypox.processing.base import processor
from pypox.processing.validators.htmx import HTMXHeaders, HTMXResponseHeaders
from starlette.testclient import TestClient
from starlette.responses import JSONResponse
from starlette.requests import Request
import pytest
from starlette.templating import Jinja2Templates
from starlette.applications import Starlette


def test_page(frontend_renderer: Jinja2Templates):

    app = Starlette()

    @processor()
    async def home(request: Request):
        return frontend_renderer.TemplateResponse(
            request=request,
            name="base.html",
        )

    app.add_route("/", home, methods=["GET"])

    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert response.text == "<h1>hello world</h1>"


def test_request(frontend_renderer: Jinja2Templates):

    app = Starlette()

    @processor()
    async def home(htmx: HTMXHeaders, request: Request):
        return frontend_renderer.TemplateResponse(
            request=request,
            name="base.html",
            headers=htmx.model_dump(by_alias=True, exclude_defaults=True),
        )

    app.add_route("/", home, methods=["GET"])  # type: ignore

    client = TestClient(app)

    response = client.get(
        "/",
        headers={
            "HX-Boosted": "true",
            "HX-Current-URL": "http://localhost/request",
            "HX-Prompt": "true",
            "HX-Request": "true",
            "HX-Target": "http://localhost/request",
            "HX-Trigger-Name": "click",
            "HX-Trigger": "mybutton",
        },
    )

    assert response.status_code == 200
    assert response.text == "<h1>hello world</h1>"
    assert response.headers["hx-boosted"] == "true"
    assert response.headers["hx-current-url"] == "http://localhost/request"
    assert response.headers["hx-prompt"] == "true"
    assert response.headers["hx-request"] == "true"
    assert response.headers["hx-target"] == "http://localhost/request"
    assert response.headers["hx-trigger-name"] == "click"
    assert response.headers["hx-trigger"] == "mybutton"


def test_response(frontend_renderer: Jinja2Templates):

    app = Starlette()

    @processor()
    async def home(request: Request):
        return frontend_renderer.TemplateResponse(
            request=request,
            name="base.html",
            headers=HTMXResponseHeaders(**request.headers).model_dump(
                by_alias=True, exclude_defaults=True
            ),
        )

    app.add_route("/", home, methods=["GET"])

    client = TestClient(app)

    response = client.get(
        "/",
        headers={
            "HX-Location": "http://localhost/request",
            "HX-Push-URL": "http://localhost/request",
            "HX-Redirect": "http://localhost/request",
            "HX-Replace-URL": "http://localhost/request",
            "HX-Reswap": "true",
            "HX-Retarget": "http://localhost/request",
            "HX-Reselect": "true",
            "HX-Trigger": "mybutton",
            "HX-Trigger-After-Settle": "click",
            "HX-Trigger-After-Swap": "click",
        },
    )
    assert response.status_code == 200
    assert response.text == "<h1>hello world</h1>"
    assert response.headers["hx-location"] == "http://localhost/request"
    assert response.headers["hx-push-url"] == "http://localhost/request"
    assert response.headers["hx-redirect"] == "http://localhost/request"
    assert response.headers["hx-replace-url"] == "http://localhost/request"
    assert response.headers["hx-reswap"] == "true"
    assert response.headers["hx-retarget"] == "http://localhost/request"
    assert response.headers["hx-reselect"] == "true"
    assert response.headers["hx-trigger"] == "mybutton"
    assert response.headers["hx-trigger-after-settle"] == "click"
    assert response.headers["hx-trigger-after-swap"] == "click"
