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

    app.add_route("/", endpoint_query, methods=["GET"]) #type: ignore
    app.add_route(
        "/query", endpoint_query_with_dash_or_underline_param, methods=["GET"] #type: ignore
    )
    app.add_route(
        "/{name}/{quantity}/{price}/{premium}", endpoint_path, methods=["GET"] #type: ignore
    )
    app.add_route("/header", endpoint_header, methods=["GET"]) #type: ignore
    app.add_route("/cookie", endpoint_cookies, methods=["GET"]) #type: ignore
    app.add_route("/json", endpoint_body, methods=["POST"]) #type: ignore

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
