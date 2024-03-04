from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from starlette.responses import JSONResponse
import base64


class BearerTokenMiddleware(BaseHTTPMiddleware):
    """
    Middleware for handling bearer token authentication.

    Args:
        app (ASGIApp): The ASGI application to wrap with the middleware.
        secret_key (str): The secret key used for token verification.
        algorithm (str): The algorithm used for token verification.
        expires_in (int, optional): The expiration time for tokens in seconds. Defaults to 3600.
    """

    def __init__(self, app, secret_key: str, algorithm: str, expires_in: int = 3600):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_in = expires_in
        super().__init__(app)

    async def dispatch(self, request, call_next):
        """Dispatches the request and performs authentication.

        Args:
            request (Request): The incoming request object.
            call_next (Callable): The next middleware or route handler.

        Returns:
            Response: The response returned by the next middleware or route handler.
        """
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
    """

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        """Dispatch method that handles the request.

        Args:
            request (Request): The incoming request.
            call_next (Callable): The next middleware or application to call.

        Returns:
            Response: The response returned by the next middleware or application.
        """
        basic, token = request.headers.get("Authorization", "").split(" ")
        if basic.lower() != "basic":
            return JSONResponse({"detail": "Invalid token type"}, status_code=401)
        username, _, password = base64.b64decode(token).decode().partition(":")
        request.state.user = {"username": username, "password": password}
        return await call_next(request)
