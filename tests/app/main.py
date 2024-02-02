import os
from pypox import Pypox

from pypox.processor.base import Query

from pypox.conventions import HTTPConvetion

app: Pypox = Pypox(
    debug=True,
    processor_func=[
        Query,
    ],
    conventions=[
        HTTPConvetion(
            directory=os.path.dirname(__file__),
        ),
    ],
)
