import os
from pypox import Pypox

from pypox.processor.base import Query, Header, Cookie, Path

from pypox.conventions import HTTPConvetion

app: Pypox = Pypox(
    debug=True,
    conventions=[
        HTTPConvetion(
            directory=os.path.dirname(__file__),
        ),
    ],
)
