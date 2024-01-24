from pypox.processor import HTMXResponse


async def endpoint(name: str):
    return HTMXResponse(
        content={
            "name": name,
        }
    )
