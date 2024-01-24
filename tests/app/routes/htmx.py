from pypox.processor import HTMXResponse
from datetime import datetime


async def endpoint(name: str):
    return HTMXResponse(
        content={
            "id": id,
            "current_time": datetime.now().strftime("%H:%M:%S"),
        }
    )
