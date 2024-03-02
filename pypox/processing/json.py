from starlette.requests import Request
from typing import Any
from pypox._types import BodyDict


class JSONValidator:

    def __init__(self, name: str, request: Request) -> None:
        self._request = request
        self._name = name

    async def __call__(self, _type: type) -> Any:
        if _type not in [BodyDict]:
            return {}
        if self._name.replace("_", "-") in self._request.cookies:
            self._value = await self._request.json()
        else:
            self._value = await self._request.json()
        return {self._name: self.validate(_type)}

    def validate(self, _type: type) -> Any:
        if _type == BodyDict:
            return dict(self._value)
        else:
            raise ValueError("Invalid type")
