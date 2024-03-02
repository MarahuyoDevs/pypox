from starlette.requests import Request
from typing import Any
from pypox._types import HeaderStr, HeaderInt, HeaderFloat, HeaderBool


class HeaderValidator:

    def __init__(self, name: str, request: Request) -> None:
        self._request = request
        self._name = name

    def __call__(self, _type: type) -> Any:
        if _type not in [HeaderStr, HeaderInt, HeaderFloat, HeaderBool]:
            return {}
        if self._name.replace("_", "-") in self._request.headers:
            self._value = self._request.headers[self._name.replace("_", "-")]
        else:
            self._value = self._request.headers[self._name.replace("-", "_")]
        return {self._name: self.validate(_type)}

    def validate(self, _type: type) -> Any:
        if _type == HeaderStr:
            return str(self._value)
        if _type == HeaderInt:
            return int(self._value)
        if _type == HeaderFloat:
            return float(self._value)
        if _type == HeaderBool:
            return bool(self._value)
