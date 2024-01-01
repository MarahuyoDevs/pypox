from tests.app.database.SQLITE import TodoDatabase
from tests.app.routes.todo.schemas import UserTodo
from sqlmodel import select
from fastapi import Depends, HTTPException, status
from pypox.database import asyncDbSession, AsyncSession


async def endpoint(user_id: str, id: str):
    """
    delete a todo
    """
    async with await asyncDbSession(TodoDatabase) as session:
        # find todo in the database
        todo = (
            (
                await session.execute(
                    select(TodoDatabase.Todo).where(
                        TodoDatabase.Todo.id == id, TodoDatabase.Todo.user_id == user_id
                    )
                )
            )
            .scalars()
            .first()
        )

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="todo not found"
            )
        # delete the todo in the database
        await session.delete(todo)
        await session.commit()

        return "Successfully deleted"
