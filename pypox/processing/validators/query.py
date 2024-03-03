from starlette.requests import Request
from typing import Any
from pypox._types import QueryStr, QueryInt, QueryFloat, QueryBool
from pypox.processing.validators.base import Validator


class QueryValidator(Validator):

    def __init__(self, name: str, _type: type) -> None:
        super().__init__(name, _type)

    async def validate(self, _type: type, request: Request) -> None:
        if _type not in [QueryStr, QueryInt, QueryFloat, QueryBool]:
            return None
        if self._name.replace("_", "-") in request.query_params:
            value = request.query_params.get(self._name.replace("_", "-"))
        else:
            value = request.query_params.get(self._name)
        if not value:
            return None
        return _type.__supertype__(value)
