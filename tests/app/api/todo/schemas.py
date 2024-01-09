from typing import Optional
from pydantic import BaseModel


class UserTodo(BaseModel):
    title: Optional[str]
    description: Optional[str]
    completed: bool


class UserTodoWithId(UserTodo):
    id: str
