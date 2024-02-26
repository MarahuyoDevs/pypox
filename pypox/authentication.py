from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from starlette.responses import JSONResponse
import base64


class BearerTokenMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, secret_key: str, algorithm: str, expires_in: int = 3600):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_in = expires_in
        super().__init__(app)

    async def dispatch(self, request, call_next):
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

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        basic, token = request.headers.get("Authorization", "").split(" ")
        if basic.lower() != "basic":
            return JSONResponse({"detail": "Invalid token type"}, status_code=401)
        username, _, password = base64.b64decode(token).decode().partition(":")
        request.state.user = {"username": username, "password": password}
        return await call_next(request)
