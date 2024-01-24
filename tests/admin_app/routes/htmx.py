from pypox.processor.htmx import HTMXResponse


async def endpoint(name: str) -> HTMXResponse:
    return HTMXResponse(
        content={
            "name": name,
        }
    )
