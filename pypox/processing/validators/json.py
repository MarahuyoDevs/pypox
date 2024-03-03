from starlette.requests import Request
from typing import Any
from pypox._types import BodyDict
from pypox.processing.validators.base import Validator


class JSONValidator(Validator):

    async def validate(self, _type: type, request: Request) -> None:
        if _type not in [BodyDict]:
            return None
        return _type.__supertype__(await request.json())
