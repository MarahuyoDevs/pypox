from pydantic import BaseModel


class Person(BaseModel):
    name: str
    age: int


async def endpoint(name: str, age: int):
    return Person(name=name, age=age)
