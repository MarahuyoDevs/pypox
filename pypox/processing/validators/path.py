from starlette.requests import Request
from typing import Any
from pypox._types import PathStr, PathInt, PathFloat, PathBool
from pypox.processing.validators.base import Validator


class PathValidator(Validator):

    def __init__(self, name: str, _type: type) -> None:
        super().__init__(name, _type)

    async def validate(self, _type: type, request: Request) -> None:
        if _type not in [PathStr, PathInt, PathFloat, PathBool]:
            return None
        if self._name.replace("_", "-") in request.path_params:
            value = request.path_params.get(self._name.replace("_", "-"))
        else:
            value = request.path_params.get(self._name)
        if not value:
            return None
        return _type.__supertype__(value)
