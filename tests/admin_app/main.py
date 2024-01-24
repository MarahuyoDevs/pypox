import os
from pypox import (
    Pypox,
)
from pypox.conventions import HTTPConvetion, HTMXConvention
from pypox.processor import (
    HTMXProcessor,
    QueryProcessor,
    PathProcessor,
    JSONProcessor,
    PydanticProcessor,
)

app: Pypox = Pypox(
    debug=True,
    processor_func=[
        QueryProcessor(),
        PathProcessor(),
        JSONProcessor(),
        PydanticProcessor(),
        HTMXProcessor(os.path.dirname(__file__) + "/routes"),
    ],
    conventions=[
        HTTPConvetion(
            directory=os.path.dirname(__file__),
        ),
        HTMXConvention(
            directory=os.path.dirname(__file__) + "/routes",
        ),
    ],
)
