"""
This module contains middleware classes for token-based authentication.

The module provides two middleware classes: `BearerTokenMiddleware` and `BasicTokenMiddleware`.
`BearerTokenMiddleware` is used for handling bearer token authentication, while `BasicTokenMiddleware`
is used for handling basic token authentication.

Classes:
    - BearerTokenMiddleware: Middleware for handling bearer token authentication.
    - BasicTokenMiddleware: Middleware for handling basic token authentication.
"""

from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.routing import BaseRoute, Match
import base64


class BearerTokenMiddleware(BaseHTTPMiddleware):
    """
    Middleware for handling bearer token authentication.

    Args:
        app (ASGIApp): The ASGI application to wrap with the middleware.
        secret_key (str): The secret key used for token verification.
        algorithm (str): The algorithm used for token verification.
        expires_in (int, optional): The expiration time for tokens in seconds. Defaults to 3600.
        routes (list[str]): The list of protected routes that require authentication.
    """

    def __init__(
        self,
        app,
        secret_key: str,
        algorithm: str,
        expires_in: int = 3600,
        routes: list[str] = [],
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_in = expires_in
        self.protected_routes = routes
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        """Dispatches the request and performs authentication.

        Args:
            request (Request): The incoming request object.
            call_next (Callable): The next middleware or route handler.

        Returns:
            Response: The response returned by the next middleware or route handler.
        """
        if not any(
            [route for route in self.protected_routes if request.url.path in route]
        ):
            return await call_next(request)

        bearer, token = request.headers.get("Authorization", "").split(" ")
        if bearer.lower() != "bearer":
            return JSONResponse({"detail": "Invalid token type"}, status_code=401)
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except ExpiredSignatureError:
            return JSONResponse({"detail": "Token has expired"}, status_code=401)
        except JWTError:
            return JSONResponse({"detail": "Invalid token"}, status_code=401)
        request.state.user = payload
        return await call_next(request)


class BasicTokenMiddleware(BaseHTTPMiddleware):
    """Middleware for handling basic token authentication.

    This middleware extracts the username and password from the Authorization header,
    validates the token type, and sets the user information in the request state.

    Args:
        app (ASGIApp): The ASGI application to wrap with this middleware.
        validator (Callable[[str, str], bool]): The validator function for validating basic tokens.
        routes (list[str]): The list of protected routes that require authentication.
    """

    def __init__(
        self,
        app,
        validator: Callable[[str, str], bool],
        routes: list[str] = [],
    ):
        self.validator = validator
        self.protected_routes = routes
        super().__init__(app)

    async def dispatch(self, request, call_next):
        """Dispatch method that handles the request.

        Args:
            request (Request): The incoming request.
            call_next (Callable): The next middleware or application to call.

        Returns:
            Response: The response returned by the next middleware or application.
        """

        if not any(
            [route for route in self.protected_routes if request.url.path in route]
        ):
            return await call_next(request)

        basic, token = request.headers.get("Authorization", "").split(" ")
        if basic.lower() != "basic":
            return JSONResponse({"detail": "Invalid token type"}, status_code=401)
        username, _, password = base64.b64decode(token).decode().partition(":")
        # call the validator function
        if not self.validator(username, password):
            return JSONResponse({"detail": "Invalid credentials"}, status_code=401)
        request.state.user = {"username": username, "password": password}
        return await call_next(request)
