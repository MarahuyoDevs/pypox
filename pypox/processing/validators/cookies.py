from starlette.requests import Request
from typing import Any
from pypox._types import CookieStr, CookieInt, CookieFloat, CookieBool
from pypox.processing.validators.base import Validator


class CookieValidator(Validator):

    async def validate(self, _type: type, request: Request) -> None:
        if _type not in [CookieStr, CookieInt, CookieFloat, CookieBool]:
            return None
        if self._name.replace("_", "-") in request.cookies:
            value = request.cookies.get(self._name.replace("_", "-"))
        else:
            value = request.cookies.get(self._name)
        if not value:
            return None
        return _type.__supertype__(value)
