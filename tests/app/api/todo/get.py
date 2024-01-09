from tests.app.database.SQLITE import TodoDatabase
from tests.app.api.todo.schemas import UserTodo, UserTodoWithId
from fastapi import status, Depends, HTTPException
from sqlmodel import select
from pypox.database import asyncDbSession, AsyncSession


async def endpoint(user_id: str):
    async with await asyncDbSession(TodoDatabase) as session:
        try:
            todo = await session.execute(
                select(TodoDatabase.Todo).where(TodoDatabase.Todo.user_id == user_id)
            )
            return [UserTodoWithId(**x.model_dump()) for x in todo.scalars().all()]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="todo not found"
            )
