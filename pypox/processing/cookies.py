from starlette.requests import Request
from typing import Any
from pypox._types import CookieStr, CookieInt, CookieFloat, CookieBool


class CookieValidator:

    def __init__(self, name: str, request: Request) -> None:
        self._request = request
        self._name = name

    def __call__(self, _type: type) -> Any:
        if _type not in [CookieStr, CookieInt, CookieFloat, CookieBool]:
            return
        if self._name.replace("_", "-") in self._request.cookies:
            self._value = self._request.cookies[self._name.replace("_", "-")]
        else:
            self._value = self._request.cookies[self._name.replace("-", "_")]
        return {self._name: self.validate(_type)}

    def validate(self, _type: type) -> Any:
        if _type == CookieStr:
            return str(self._value)
        if _type == CookieInt:
            return int(self._value)
        if _type == CookieFloat:
            return float(self._value)
        if _type == CookieBool:
            return bool(self._value)
