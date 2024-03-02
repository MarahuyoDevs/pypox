from starlette.requests import Request
from typing import Any
from pypox._types import QueryStr, QueryInt, QueryFloat, QueryBool


class QueryValidator:

    def __init__(self, name: str, request: Request) -> None:
        self._request = request
        self._name = name

    def __call__(self, _type: type) -> Any:
        if _type not in [QueryStr, QueryInt, QueryFloat, QueryBool]:
            return {}
        if self._name.replace("_", "-") in self._request.query_params:
            self._value = self._request.query_params[self._name.replace("_", "-")]
        else:
            self._value = self._request.query_params[self._name.replace("-", "_")]
        return {self._name: self.validate(_type)}

    def validate(self, _type: type) -> Any:
        if _type == QueryStr:
            return str(self._value)
        if _type == QueryInt:
            return int(self._value)
        if _type == QueryFloat:
            return float(self._value)
        if _type == QueryBool:
            return bool(self._value)
