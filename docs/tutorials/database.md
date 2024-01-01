Pypox simplifies database management using `sqlmodel` and `sqlalchemy`, adhering to the DBAPI 2.0 specification common in the Python ecosystem. This tutorial will guide you through setting up and using a database in Pypox.

#### Setting Up the Database

- **Creating the Database Structure:**
  Start by creating a folder named `database` within your Pypox project directory. Inside this folder, create another folder named `SQLITE` (representing the database system to use).

!!! info

    The folder name convention helps Pypox identify the type of database you intend to connect to. you can use other database such as `POSTGRESQL`, `ORACLE`, `MYSQL` etc.

- **Generating Database Files:**
  Inside the `SQLITE` folder, create a Python file adhering to the naming convention `Db.py` (or any name you prefer). This Python file will generate the database. For instance, `sampleDb.py` will result in a database named `sampleDb.db` as we're using SQLite for this example.

  ```
  pypox_sample/
  |
  └─── database/
       └───SQLITE/
           └───sampleDb.py
   ...
  ```

- **Defining Tables:**
  Within the `Db.py` file, define a SQLModel table using `sqlmodel`. Here's an example:

  ```python
  from sqlmodel import SQLModel, Field

  class SampleTable(SQLModel, table=True):
      id: int = Field(primary_key=True)
      name: str
      age: str
  ```

#### Integration with Pypox

1. **Initializing the Database Engine:**
   Navigate to the `startup.py` file in your project folder. This file manages the startup and shutdown events for the application.
   Inside the `__call__` function in `startup.py`, import the database you created (`sampleDb`) and use `createAsyncEngine()` to initialize the database engine.

   ```python
   from pypox import createAsyncEngine
   from pypox_sample.database.SQLITE import sampleDb

   async def __call__(app: FastAPI):
       # Create an engine and store it in a context var
       createAsyncEngine(sampleDb)
   ```

2. **Database Usage in Endpoints:**
   Let's use the database in an endpoint (e.g., `routes/user/get.py`). Import the necessary function `asyncDbSession` and the database (`sampleDb`) and leverage it within an endpoint function.

   ```python
   from pypox import asyncDbSession
   from pypox_sample.database.SQLITE import sampleDb

   async def endpoint():
       # this will get the engine that we created earlier from the startup.py and use it as a session
       async with await asyncDbSession(sampleDb) as session:
           # Perform database operations (e.g., query data)
           return {"message": "Database is now operational!"}
   ```

By following these steps, you can seamlessly integrate and leverage databases within your Pypox project. Pypox simplifies database initialization, connection management, and CRUD operations, enabling efficient database interactions within your application.
