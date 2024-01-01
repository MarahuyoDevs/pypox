#### create_engine_sync

```python
async def create_engine_sync(module, username: str = "", password: str = "", host: str = "", port: str = "", **kwargs) -> Engine:
```

Creates a synchronous SQLAlchemy engine based on the provided module and connection parameters.

- **Parameters:**
  - `module`: The module object representing the database driver.
  - `username` (str): The username for the database connection (default: "").
  - `password` (str): The password for the database connection (default: "").
  - `host` (str): The host address for the database connection (default: "").
  - `port` (str): The port number for the database connection (default: "").
  - `**kwargs`: Additional keyword arguments for the SQLAlchemy create_engine function.
- **Returns:** An SQLAlchemy engine object.
- **Raises:** None.

---

#### create_engine_async

```python
def create_engine_async(module, driver, username: str = "", password: str = "", host: str = "", port: str = "", **kwargs) -> AsyncEngine
```

Creates an asynchronous SQLAlchemy engine based on the provided module, driver, and connection parameters.

- **Parameters:**
  - `module`: The module object representing the database dialect.
  - `driver`: The database driver to be used.
  - `username` (str): The username for the database connection (optional).
  - `password` (str): The password for the database connection (optional).
  - `host` (str): The host address for the database connection (optional).
  - `port` (str): The port number for the database connection (optional).
  - `**kwargs`: Additional keyword arguments for the SQLAlchemy engine.
- **Returns:** An asynchronous SQLAlchemy engine object.
- **Raises:** None.

---

#### init_database_sync

```python
async def init_database_sync(engine, module) -> None:
```

Initializes the database by creating all tables defined in the SQLModel metadata.

- **Parameters:**
  - `engine` (sqlalchemy.engine.Engine): The SQLAlchemy engine object.
  - `module` (module): The module containing the SQLModel metadata.
- **Returns:** None.

---

#### init_database_async

```python
async def init_database_async(engine: AsyncEngine, module: Any) -> None:
```

Initialize the database asynchronously.

- **Parameters:**
  - `engine` (AsyncEngine): The SQLAlchemy async engine instance.
  - `module` (Any): The module containing the SQLModel metadata.
- **Returns:** None.

---

#### createSyncEngine

```python
def createSyncEngine(module: ModuleType, **kwargs) -> None:
```

Create a new engine and add it to the context variable.

- **Parameters:**
  - `module` (ModuleType): The module to create the engine for.
  - `**kwargs`: Additional keyword arguments for the create_engine_sync function.
- **Returns:** None.

---

#### createAsyncEngine

```python
def createAsyncEngine(module: ModuleType, driver: str, **kwargs) -> None:
```

Create a new engine and add it to the context variable.

- **Parameters:**
  - `module` (ModuleType): The module containing the database driver.
  - `driver` (str): The name of the database driver.
  - `**kwargs`: Additional keyword arguments for the create_engine_async function.
- **Returns:** None.

---

#### getSyncEngine

```python
def getSyncEngine(database: ModuleType | str) -> Engine
```

Retrieves the sync engine for the specified database.

- **Parameters:**
  - `database` (ModuleType | str): The database module or name.
- **Returns:** The sync engine for the specified database.

---

#### getAsyncEngine

```python
def getAsyncEngine(database: ModuleType | str) -> AsyncEngine
```

Retrieves the asynchronous engine for the specified database.

- **Parameters:**
  - `database` (ModuleType | str): The database module or name.
- **Returns:** The asynchronous engine for the specified database.

---

#### asyncDbSession

```python
def asyncDbSession(database: ModuleType | str) -> AsyncSession:
```

Create an asynchronous database session.

- **Parameters:**
  - `database` (ModuleType | str): The database module or the name of the database.
- **Returns:** The asynchronous database session.

---

#### syncDbSession

```python
def syncDbSession(database: ModuleType | str) -> Session:
```

Create and return a synchronized database session.

- **Parameters:**
  - `database` (ModuleType | str): The database module or the name of the database.
- **Returns:** A synchronized database session.

---
