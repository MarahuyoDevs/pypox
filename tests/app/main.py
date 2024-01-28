import os
from pypox import Pypox

from pypox.processor.base import (
    query_processor,
    path_processor,
    json_processor,
)
from pypox.processor.pydantic import pydantic_processor

from pypox.conventions import HTTPConvetion

app: Pypox = Pypox(
    debug=True,
    processor_func=[
        query_processor,
        path_processor,
        json_processor,
        pydantic_processor,
    ],
    conventions=[
        HTTPConvetion(
            directory=os.path.dirname(__file__),
        ),
    ],
)
