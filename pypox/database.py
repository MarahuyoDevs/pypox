import asyncio
import os
from types import ModuleType
from typing import Any, Optional
from sqlalchemy import Engine
from sqlmodel import create_engine as alchemy_create_engine
from sqlalchemy.ext.asyncio import (
    create_async_engine as alchemy_create_engine_async,
    AsyncEngine,
    AsyncSession,
)
from sqlalchemy.orm import Session
from contextvars import ContextVar

engines_sync: ContextVar[dict[str, Engine]] = ContextVar("engines_sync")
engines_async: ContextVar[dict[str, AsyncEngine]] = ContextVar("engines_async")


def create_engine_sync(
    module,
    username: str = "",
    password: str = "",
    host: str = "",
    port: str = "",
    **kwargs,
):
    """
    Create a synchronous SQLAlchemy engine based on the provided module and connection parameters.

    Args:
        module: The module object representing the database driver.
        username: The username for the database connection (default: "").
        password: The password for the database connection (default: "").
        host: The host address for the database connection (default: "").
        port: The port number for the database connection (default: "").
        **kwargs: Additional keyword arguments to be passed to the SQLAlchemy create_engine function.

    Returns:
        An SQLAlchemy engine object.

    Raises:
        None.
    """
    # get the name
    db_name = module.__name__.split(".")[-1].lower()
    dialect = module.__name__.split(".")[-2].lower()
    db_path = (
        os.path.dirname(module.__file__).replace(os.getcwd(), "").replace("\\", "/")
    )
    # connect to database

    if dialect == "sqlite":
        return alchemy_create_engine(f"{dialect}://{db_path}/{db_name}.db", **kwargs)
    else:
        return alchemy_create_engine(
            f"{dialect}://{username}:{password}@{host}:{port}/{db_name}", **kwargs
        )


def create_engine_async(module, driver, username: str = "", password: str = "", host: str = "", port: str = "", **kwargs) -> AsyncEngine:  # type: ignore
    """
    Create an asynchronous SQLAlchemy engine based on the provided module, driver, and connection parameters.

    Args:
        module: The module object representing the database dialect.
        driver: The database driver to be used.
        username: The username for the database connection (optional).
        password: The password for the database connection (optional).
        host: The host address for the database connection (optional).
        port: The port number for the database connection (optional).
        **kwargs: Additional keyword arguments to be passed to the SQLAlchemy engine.

    Returns:
        An asynchronous SQLAlchemy engine object.

    Raises:
        None.

    """
    db_name = module.__name__.split(".")[-1].lower()
    dialect = module.__name__.split(".")[-2].lower()
    db_path = (
        os.path.dirname(module.__file__).replace(os.getcwd(), "").replace("\\", "/")
    )
    if dialect == "sqlite":
        return alchemy_create_engine_async(
            f"{dialect}+{driver}://{db_path}/{db_name}.db", **kwargs
        )
    else:
        return alchemy_create_engine_async(
            f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{db_name}",
            **kwargs,
        )


def init_database_sync(engine, module):
    """
    Initializes the database by creating all the tables defined in the SQLModel metadata.

    Args:
        engine (sqlalchemy.engine.Engine): The SQLAlchemy engine object.
        module (module): The module containing the SQLModel metadata.

    Returns:
        None
    """
    module.SQLModel.metadata.create_all(engine)


async def init_database_async(engine: AsyncEngine, module: Any) -> None:
    """
    Initialize the database asynchronously.

    Args:
        engine (AsyncEngine): The SQLAlchemy async engine instance.
        module (Any): The module containing the SQLModel metadata.

    Returns:
        None
    """
    async with engine.begin() as connection:
        await connection.run_sync(module.SQLModel.metadata.create_all)


def createSyncEngine(module: ModuleType, **kwargs):
    """
    Create a new engine and add it to the context variable.

    Args:
        module (ModuleType): The module to create the engine for.
        **kwargs: Additional keyword arguments to pass to the create_engine_sync function.

    Returns:
        None
    """

    engine = create_engine_sync(module, **kwargs)

    engines_dict: dict[str, Engine] = engines_sync.get({})

    engines_dict[module.__name__.split(".")[-1].lower()] = engine

    engines_sync.set(engines_dict)


def createAsyncEngine(module: ModuleType, driver: str, **kwargs):
    """
    Create a new engine and add it to the context variable.

    Args:
        module (ModuleType): The module containing the database driver.
        driver (str): The name of the database driver.
        **kwargs: Additional keyword arguments to be passed to the create_engine_async function.

    Returns:
        None
    """
    engine = create_engine_async(module, driver, **kwargs)

    engines_dict: dict[str, AsyncEngine] = engines_async.get({})

    engines_dict[module.__name__.split(".")[-1].lower()] = engine

    engines_async.set(engines_dict)
    return


def getSyncEngine(database: ModuleType | str) -> Engine:
    """
    Retrieves the sync engine for the specified database.

    Parameters:
        database (ModuleType | str): The database module or name.

    Returns:
        Engine: The sync engine for the specified database.
    """
    if isinstance(database, str):
        engine: Engine = engines_sync.get()[database.lower()]
    elif isinstance(database, ModuleType):
        engine: Engine = engines_sync.get()[database.__name__.split(".")[-1].lower()]
    return engine


def getAsyncEngine(database: ModuleType | str) -> AsyncEngine:
    """
    Retrieves the asynchronous engine for the specified database.

    Args:
        database (ModuleType | str): The database module or name.

    Returns:
        AsyncEngine: The asynchronous engine for the specified database.
    """
    if isinstance(database, str):
        engine: AsyncEngine = engines_async.get()[database.lower()]
    elif isinstance(database, ModuleType):
        engine: AsyncEngine = engines_async.get()[
            database.__name__.split(".")[-1].lower()
        ]
    return engine


async def asyncDbSession(database: ModuleType | str) -> AsyncSession:
    """
    Create an asynchronous database session.

    Args:
        database (ModuleType | str): The database module or the name of the database.

    Returns:
        AsyncSession: The asynchronous database session.

    """
    # get the engine
    if isinstance(database, str):
        engine: AsyncEngine = getAsyncEngine(database)
    elif isinstance(database, ModuleType):
        engine: AsyncEngine = getAsyncEngine(database.__name__.split(".")[-1].lower())
    return AsyncSession(engine)


def syncDbSession(database: ModuleType | str) -> Session:
    """
    Create and return a synchronized database session.

    Parameters:
    - database: Either a string representing the name of the database or a ModuleType object.
                If a string is provided, it will be used to retrieve the engine.
                If a ModuleType object is provided, its name will be used to retrieve the engine.

    Returns:
    - Session: A synchronized database session.

    """
    # get the engine
    if isinstance(database, str):
        engine: Engine = getSyncEngine(database)
    elif isinstance(database, ModuleType):
        engine: Engine = getSyncEngine(database.__name__.split(".")[-1].lower())

    return Session(engine)
