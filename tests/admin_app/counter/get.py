counter_data = {"counter": 0}


async def endpoint():
    counter_data["counter"] += 1
    return counter_data["counter"]
