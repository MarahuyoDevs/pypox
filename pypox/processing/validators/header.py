from starlette.requests import Request
from typing import Any
from pypox._types import HeaderStr, HeaderInt, HeaderFloat, HeaderBool
from pypox.processing.validators.base import Validator


class HeaderValidator(Validator):

    def __init__(self, name: str, _type: type) -> None:
        super().__init__(name, _type)

    async def validate(self, _type: type, request: Request) -> None:
        if _type not in [HeaderStr, HeaderInt, HeaderFloat, HeaderBool]:
            return None
        if self._name.replace("_", "-") in request.headers:
            value = request.headers.get(self._name.replace("_", "-"))
        else:
            value = request.headers.get(self._name)
        if not value:
            return None
        return _type.__supertype__(value)
