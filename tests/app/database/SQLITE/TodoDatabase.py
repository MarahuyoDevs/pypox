from sqlmodel import SQLModel, Field
from typing import Optional


class Todo(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    title: str
    description: str
    completed: bool
    user_id: Optional[str] = Field(default=None, foreign_key="user.id")


class User(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    username: str
    password: str
    name: str
    email: str
    phone: str
