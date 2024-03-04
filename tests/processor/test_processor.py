import pytest
from starlette.responses import JSONResponse
from pypox._types import (
    BodyDict,
    PathBool,
    PathFloat,
    PathInt,
    PathStr,
    QueryStr,
    QueryBool,
    QueryFloat,
    QueryInt,
    HeaderBool,
    HeaderFloat,
    HeaderInt,
    HeaderStr,
    CookieBool,
    CookieFloat,
    CookieInt,
    CookieStr,
)
from pypox.application import Pypox
from pypox.processing.base import processor
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.testclient import TestClient
from starlette.exceptions import HTTPException

from pypox.processing.validators.htmx import (
    HTMXHeaders,
    HTMXResponseHeaders,
    HTMXValidator,
)


@pytest.fixture
def api_client():

    app = Starlette()

    @processor()
    async def endpoint_query(
        name: QueryStr, quantity: QueryInt, price: QueryFloat, premium: QueryBool
    ) -> JSONResponse:
        """
        This is a test endpoint.
        """
        if not name:
            raise HTTPException(status_code=400, detail="Name is required.")

        if not quantity:
            raise HTTPException(status_code=400, detail="Quantity is required.")

        if not price:
            raise HTTPException(status_code=400, detail="Price is required.")

        return JSONResponse(
            {
                "name": name,
                "quantity": quantity,
                "price": price,
                "premium": premium,
            }
        )

    @processor()
    async def endpoint_query_with_dash_or_underline_param(
        name_str: QueryStr,
        quantity_int: QueryInt,
        price_float: QueryFloat,
        premium_bool: QueryBool,
    ) -> JSONResponse:
        """
        This is a test endpoint.
        """
        if not name_str:
            raise HTTPException(status_code=400, detail="Name is required.")

        if not quantity_int:
            raise HTTPException(status_code=400, detail="Quantity is required.")

        if not price_float:
            raise HTTPException(status_code=400, detail="Price is required.")

        return JSONResponse(
            {
                "name": name_str,
                "quantity": quantity_int,
                "price": price_float,
                "premium": premium_bool,
            }
        )

    @processor()
    async def endpoint_path(
        name: PathStr, quantity: PathInt, price: PathFloat, premium: PathBool
    ) -> JSONResponse:
        """
        This is a test endpoint.
        """
        if not name:
            raise HTTPException(status_code=400, detail="Name is required.")

        if not quantity:
            raise HTTPException(status_code=400, detail="Quantity is required.")

        if not price:
            raise HTTPException(status_code=400, detail="Price is required.")

        return JSONResponse(
            {
                "name": name,
                "quantity": quantity,
                "price": price,
                "premium": premium,
            }
        )

    @processor()
    async def endpoint_header(
        header_name: HeaderStr,
        header_quantity: HeaderInt,
        header_price: HeaderFloat,
        header_premium: HeaderBool,
    ) -> JSONResponse:
        """
        This is a test endpoint.
        """
        return JSONResponse(
            {
                "name": header_name,
                "quantity": header_quantity,
                "price": header_price,
                "premium": header_premium,
            }
        )

    @processor()
    async def endpoint_cookies(
        cookie_name: CookieStr,
        cookie_quantity: CookieInt,
        cookie_price: CookieFloat,
        cookie_premium: CookieBool,
    ) -> JSONResponse:
        """
        This is a test endpoint.
        """
        return JSONResponse(
            {
                "name": cookie_name,
                "quantity": cookie_quantity,
                "price": cookie_price,
                "premium": cookie_premium,
            }
        )

    @processor()
    async def endpoint_body(body: BodyDict) -> JSONResponse:
        return JSONResponse(body)

    app.add_route("/", endpoint_query, methods=["GET"])  # type: ignore
    app.add_route(
        "/query", endpoint_query_with_dash_or_underline_param, methods=["GET"]  # type: ignore
    )
    app.add_route(
        "/{name}/{quantity}/{price}/{premium}", endpoint_path, methods=["GET"]  # type: ignore
    )
    app.add_route("/header", endpoint_header, methods=["GET"])  # type: ignore
    app.add_route("/cookie", endpoint_cookies, methods=["GET"])  # type: ignore
    app.add_route("/json", endpoint_body, methods=["POST"])  # type: ignore

    yield TestClient(
        app,
        headers={
            "header-name": "apple",
            "header-quantity": "2",
            "header-price": "1.5",
            "header-premium": "true",
        },
        cookies={
            "cookie-name": "apple",
            "cookie-quantity": "2",
            "cookie-price": "1.5",
            "cookie-premium": "true",
        },
    )


@pytest.fixture
def pypox_client():

    app = Pypox()

    async def endpoint_query(
        name: QueryStr, quantity: QueryInt, price: QueryFloat, premium: QueryBool
    ) -> JSONResponse:
        """
        This is a test endpoint.
        """
        if not name:
            raise HTTPException(status_code=400, detail="Name is required.")

        if not quantity:
            raise HTTPException(status_code=400, detail="Quantity is required.")

        if not price:
            raise HTTPException(status_code=400, detail="Price is required.")

        return JSONResponse(
            {
                "name": name,
                "quantity": quantity,
                "price": price,
                "premium": premium,
            }
        )

    async def endpoint_query_with_dash_or_underline_param(
        name_str: QueryStr,
        quantity_int: QueryInt,
        price_float: QueryFloat,
        premium_bool: QueryBool,
    ) -> JSONResponse:
        """
        This is a test endpoint.
        """
        if not name_str:
            raise HTTPException(status_code=400, detail="Name is required.")

        if not quantity_int:
            raise HTTPException(status_code=400, detail="Quantity is required.")

        if not price_float:
            raise HTTPException(status_code=400, detail="Price is required.")

        return JSONResponse(
            {
                "name": name_str,
                "quantity": quantity_int,
                "price": price_float,
                "premium": premium_bool,
            }
        )

    async def endpoint_path(
        name: PathStr, quantity: PathInt, price: PathFloat, premium: PathBool
    ) -> JSONResponse:
        """
        This is a test endpoint.
        """
        if not name:
            raise HTTPException(status_code=400, detail="Name is required.")

        if not quantity:
            raise HTTPException(status_code=400, detail="Quantity is required.")

        if not price:
            raise HTTPException(status_code=400, detail="Price is required.")

        return JSONResponse(
            {
                "name": name,
                "quantity": quantity,
                "price": price,
                "premium": premium,
            }
        )

    async def endpoint_header(
        header_name: HeaderStr,
        header_quantity: HeaderInt,
        header_price: HeaderFloat,
        header_premium: HeaderBool,
    ) -> JSONResponse:
        """
        This is a test endpoint.
        """
        return JSONResponse(
            {
                "name": header_name,
                "quantity": header_quantity,
                "price": header_price,
                "premium": header_premium,
            }
        )

    async def endpoint_cookies(
        cookie_name: CookieStr,
        cookie_quantity: CookieInt,
        cookie_price: CookieFloat,
        cookie_premium: CookieBool,
    ) -> JSONResponse:
        """
        This is a test endpoint.
        """
        return JSONResponse(
            {
                "name": cookie_name,
                "quantity": cookie_quantity,
                "price": cookie_price,
                "premium": cookie_premium,
            }
        )

    async def endpoint_body(body: BodyDict) -> JSONResponse:
        return JSONResponse(body)

    app.add_route("/", endpoint_query, methods=["GET"])
    app.add_route(
        "/query", endpoint_query_with_dash_or_underline_param, methods=["GET"]
    )
    app.add_route(
        "/{name}/{quantity}/{price}/{premium}", endpoint_path, methods=["GET"]
    )
    app.add_route("/header", endpoint_header, methods=["GET"])
    app.add_route("/cookie", endpoint_cookies, methods=["GET"])
    app.add_route("/json", endpoint_body, methods=["POST"])

    yield TestClient(
        app,
        headers={
            "header-name": "apple",
            "header-quantity": "2",
            "header-price": "1.5",
            "header-premium": "true",
        },
        cookies={
            "cookie-name": "apple",
            "cookie-quantity": "2",
            "cookie-price": "1.5",
            "cookie-premium": "true",
        },
    )


@pytest.fixture
def htmx_client():

    @processor([HTMXValidator])
    async def htmx_request(htmx: HTMXHeaders) -> JSONResponse:
        return JSONResponse(htmx.model_dump())

    async def htmx_response(request: Request) -> JSONResponse:
        return JSONResponse(HTMXResponseHeaders(**request.headers).model_dump())

    app = Starlette()

    app.add_route("/", htmx_request, methods=["GET"])  # type: ignore
    app.add_route("/response", processor()(htmx_response), methods=["GET"])

    return TestClient(app)


class TestBaseProcessor:

    def test_query_processor(self, api_client: TestClient):
        response = api_client.get("/?name=apple&quantity=2&price=1.5&premium=true")
        assert response.status_code == 200
        assert response.json() == {
            "name": "apple",
            "quantity": 2,
            "price": 1.5,
            "premium": True,
        }

    def test_query_processor_with_dash_params(self, api_client: TestClient):
        response = api_client.get(
            "/query/?name-str=apple&quantity-int=2&price-float=1.5&premium-bool=true"
        )
        assert response.status_code == 200
        assert response.json() == {
            "name": "apple",
            "quantity": 2,
            "price": 1.5,
            "premium": True,
        }

    def test_query_processor_with_underline_params(self, api_client: TestClient):
        response = api_client.get(
            "/query/?name_str=apple&quantity_int=2&price_float=1.5&premium_bool=true"
        )
        assert response.status_code == 200
        assert response.json() == {
            "name": "apple",
            "quantity": 2,
            "price": 1.5,
            "premium": True,
        }

    def test_path_processor(self, api_client: TestClient):
        response = api_client.get("/apple/2/1.5/true")
        assert response.status_code == 200
        assert response.json() == {
            "name": "apple",
            "quantity": 2,
            "price": 1.5,
            "premium": True,
        }

    def test_header_processor(self, api_client: TestClient):
        response = api_client.get(
            "/header",
        )
        assert response.status_code == 200
        assert response.json() == {
            "name": "apple",
            "quantity": 2,
            "price": 1.5,
            "premium": True,
        }

    def test_cookie_processor(self, api_client: TestClient):
        response = api_client.get(
            "/cookie",
        )
        assert response.status_code == 200
        assert response.json() == {
            "name": "apple",
            "quantity": 2,
            "price": 1.5,
            "premium": True,
        }

    def test_body_processor(self, api_client: TestClient):
        response = api_client.post(
            "/json",
            json={
                "name": "apple",
                "quantity": 2,
                "price": 1.5,
                "premium": True,
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            "name": "apple",
            "quantity": 2,
            "price": 1.5,
            "premium": True,
        }


class TestPypoxProcessor:

    def test_query_processor(self, pypox_client: TestClient):
        response = pypox_client.get("/?name=apple&quantity=2&price=1.5&premium=true")
        assert response.status_code == 200
        assert response.json() == {
            "name": "apple",
            "quantity": 2,
            "price": 1.5,
            "premium": True,
        }

    def test_query_processor_with_dash_params(self, pypox_client: TestClient):
        response = pypox_client.get(
            "/query/?name-str=apple&quantity-int=2&price-float=1.5&premium-bool=true"
        )
        assert response.status_code == 200
        assert response.json() == {
            "name": "apple",
            "quantity": 2,
            "price": 1.5,
            "premium": True,
        }

    def test_query_processor_with_underline_params(self, pypox_client: TestClient):
        response = pypox_client.get(
            "/query/?name_str=apple&quantity_int=2&price_float=1.5&premium_bool=true"
        )
        assert response.status_code == 200
        assert response.json() == {
            "name": "apple",
            "quantity": 2,
            "price": 1.5,
            "premium": True,
        }

    def test_path_processor(self, pypox_client: TestClient):
        response = pypox_client.get("/apple/2/1.5/true")
        assert response.status_code == 200
        assert response.json() == {
            "name": "apple",
            "quantity": 2,
            "price": 1.5,
            "premium": True,
        }

    def test_header_processor(self, pypox_client: TestClient):
        response = pypox_client.get(
            "/header",
        )
        assert response.status_code == 200
        assert response.json() == {
            "name": "apple",
            "quantity": 2,
            "price": 1.5,
            "premium": True,
        }

    def test_cookie_processor(self, pypox_client: TestClient):
        response = pypox_client.get(
            "/cookie",
        )
        assert response.status_code == 200
        assert response.json() == {
            "name": "apple",
            "quantity": 2,
            "price": 1.5,
            "premium": True,
        }

    def test_body_processor(self, pypox_client: TestClient):
        response = pypox_client.post(
            "/json",
            json={
                "name": "apple",
                "quantity": 2,
                "price": 1.5,
                "premium": True,
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            "name": "apple",
            "quantity": 2,
            "price": 1.5,
            "premium": True,
        }


class TestHTMX:

    def test_htmx_headers(self, htmx_client: TestClient):
        response = htmx_client.get(
            "/",
            headers={
                "HX-Boosted": "true",
                "HX-Current-Url": "http://localhost:8000",
                "HX-History-Restored": "true",
                "HX-Prompt": "true",
                "HX-Request": "true",
                "HX-Target": "target",
                "HX-Trigger-name": "trigger-name",
                "HX-Trigger": "trigger",
            },
        )
        assert response.json() == {
            "boosted": "true",
            "current_url": "http://localhost:8000",
            "history_restored": "true",
            "prompt": "true",
            "request": "true",
            "target": "target",
            "trigger_name": "trigger-name",
            "trigger": "trigger",
        }

    def test_htmx_response_headers(self, htmx_client: TestClient):
        response = htmx_client.get(
            "/response",
            headers={
                "HX-Location": "http://localhost:8000",
                "HX-Push-Url": "http://localhost:8000",
                "HX-Redirect": "http://localhost:8000",
                "HX-Refresh": "http://localhost:8000",
                "HX-Replace-Url": "http://localhost:8000",
                "HX-Reswap": "http://localhost:8000",
                "HX-Retarget": "http://localhost:8000",
                "HX-Reselect": "http://localhost:8000",
                "HX-Trigger": "http://localhost:8000",
                "HX-Trigger-After-Settle": "http://localhost:8000",
                "HX-Trigger-After-Swap": "http://localhost:8000",
            },
        )
        assert response.json() == {
            "location": "http://localhost:8000",
            "push_url": "http://localhost:8000",
            "redirect": "http://localhost:8000",
            "refresh": "http://localhost:8000",
            "replace_url": "http://localhost:8000",
            "reswap": "http://localhost:8000",
            "retarget": "http://localhost:8000",
            "reselect": "http://localhost:8000",
            "trigger": "http://localhost:8000",
            "trigger_after_settle": "http://localhost:8000",
            "trigger_after_swap": "http://localhost:8000",
        }
