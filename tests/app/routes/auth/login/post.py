from sqlalchemy import Row
from fastapi import status, HTTPException
from pypox.database import asyncDbSession, AsyncSession
from tests.app.routes.auth.login.schemas import UserLogin
from tests.app.database.SQLITE import TodoDatabase
from sqlmodel import select


async def endpoint(body: UserLogin):
    """
    login the user
    """
    async with await asyncDbSession(TodoDatabase) as session:
        # check if the user exist in the database
        user: Row[tuple[TodoDatabase.User]] | None = (
            await session.execute(
                select(TodoDatabase.User).where(
                    TodoDatabase.User.username == body.username
                )
            )
        ).one()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Incorrect username or password",
            )

        return user[0].id
