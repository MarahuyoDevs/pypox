from starlette.requests import Request
from typing import Any
from pypox._types import BodyForm


class FormValidator:

    def __init__(self, name: str, request: Request) -> None:
        self._request = request
        self._name = name

    async def __call__(self, _type: type) -> Any:
        if _type not in [BodyForm]:
            return {}
        if self._name.replace("_", "-") in self._request.cookies:
            self._value = await self._request.form()
        else:
            self._value = await self._request.form()
        return {self._name: self.validate(_type)}

    def validate(self, _type: type) -> Any:
        if _type == BodyForm:
            return dict(self._value)
        else:
            raise ValueError("Invalid type")
