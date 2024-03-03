from abc import ABC
from starlette.requests import Request


class Validator(ABC):

    def __init__(self, name: str, _type: type) -> None:
        self._name = name
        self._type = _type

    @property
    def name(self) -> str:
        return self._name

    async def validate(self, _type: type, request: Request) -> None:
        raise NotImplementedError("validate method must be implemented")

    async def __call__(self, request: Request) -> dict:
        value = await self.validate(self._type, request)
        if not value:
            return {}
        else:
            return {self._name: value}
