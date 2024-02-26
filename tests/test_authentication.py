import base64
from starlette.applications import Starlette
from starlette.requests import Request
from pypox.authentication import BearerTokenMiddleware, BasicTokenMiddleware
from starlette.responses import JSONResponse
from starlette.testclient import TestClient
from jose import jwt

bearer_token_app = Starlette()


bearer_token_app.add_middleware(
    BearerTokenMiddleware, secret_key="secret", algorithm="HS256", expires_in=3600
)


@bearer_token_app.route("/", methods=["GET"])
async def index(request: Request) -> JSONResponse:
    return JSONResponse({"detail": "Authenticated", "user": request.state.user})


class TestBearerTokenMiddleware:

    client = TestClient(bearer_token_app)

    def test_authentication(self):
        token = jwt.encode({"payload": "data"}, "secret", algorithm="HS256")
        response = self.client.get("/", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.json() == {
            "detail": "Authenticated",
            "user": {"payload": "data"},
        }


basic_token_app = Starlette()


basic_token_app.add_middleware(BasicTokenMiddleware)


@basic_token_app.route("/", methods=["GET"])
async def basic_token_index(request: Request) -> JSONResponse:
    return JSONResponse({"detail": "Authenticated", "user": request.state.user})


class TestBasicTokenMiddleware:

    client = TestClient(basic_token_app)

    def test_authentication(self):
        credentials = base64.b64encode("username:password".encode()).decode("utf-8")
        response = self.client.get(
            "/", headers={"Authorization": f"Basic {credentials}"}
        )
        assert response.status_code == 200
        assert response.json() == {
            "detail": "Authenticated",
            "user": {"username": "username", "password": "password"},
        }
