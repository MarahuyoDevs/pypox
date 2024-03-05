import base64
import pytest
from starlette.applications import Starlette
from starlette.requests import Request
from pypox.authentication import BearerTokenMiddleware, BasicTokenMiddleware
from starlette.responses import JSONResponse
from starlette.testclient import TestClient
from jose import jwt


@pytest.fixture
def bearer_client():
    app = Starlette()

    app.add_middleware(
        BearerTokenMiddleware,
        secret_key="secret",
        algorithm="HS256",
        expires_in=3600,
        routes=["/protected"],
    )

    async def protected_route(request: Request) -> JSONResponse:
        return JSONResponse({"detail": "Authenticated", "user": request.state.user})

    async def public_route(request: Request) -> JSONResponse:
        return JSONResponse({"detail": "Public"})

    app.add_route("/protected", protected_route, methods=["GET"])
    app.add_route("/public", public_route, methods=["GET"])

    return TestClient(app)


@pytest.fixture
def basic_client():

    app = Starlette()

    app.add_middleware(
        BasicTokenMiddleware,
        routes=["/protected"],
        validator=lambda username, password: username == "username"
        and password == "password",
    )

    async def protected_route(request: Request) -> JSONResponse:
        return JSONResponse({"detail": "Authenticated", "user": request.state.user})

    async def public_route(request: Request) -> JSONResponse:
        return JSONResponse({"detail": "Public"})

    app.add_route("/protected", protected_route, methods=["GET"])
    app.add_route("/public", public_route, methods=["GET"])

    return TestClient(app)


class TestBearerTokenMiddleware:

    def test_authentication(self, bearer_client: TestClient):
        token = jwt.encode({"payload": "data"}, "secret", algorithm="HS256")
        response = bearer_client.get(
            "/protected", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json() == {
            "detail": "Authenticated",
            "user": {"payload": "data"},
        }

    def test_public_route(self, bearer_client: TestClient):
        response = bearer_client.get("/public")
        assert response.status_code == 200
        assert response.json() == {"detail": "Public"}


class TestBasicTokenMiddleware:

    def test_protected_authentication(self, basic_client: TestClient):
        credentials = base64.b64encode("username:password".encode()).decode("utf-8")
        response = basic_client.get(
            "/protected", headers={"Authorization": f"Basic {credentials}"}
        )
        assert response.status_code == 200
        assert response.json() == {
            "detail": "Authenticated",
            "user": {"username": "username", "password": "password"},
        }

    def test_public_authentication(self, basic_client: TestClient):
        response = basic_client.get("/public")
        assert response.status_code == 200
        assert response.json() == {
            "detail": "Public",
        }
