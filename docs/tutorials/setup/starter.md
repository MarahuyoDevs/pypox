Pypox is a powerful convention-based API framework that simplifies API development on FastAPI. It can be easily installed using Poetry, a Python dependency management and packaging tool.

### Installing Poetry

Firstly, ensure Poetry is installed on your local machine. You can install Poetry by following the official instructions [here](https://python-poetry.org/docs/#installation).

### Adding Pypox as a Dependency

Once Poetry is set up, you can add Pypox to your project's dependencies. Run the following command in your terminal:

```bash
poetry add pypox
```

This command will not only add Pypox but also install all necessary dependencies such as `FastAPI`, `SQLModel`, `SQLAlchemy`, and `Uvicorn (standard version)`. If you prefer using a different ASGI web server, you're free to install and use it instead.

!!! note

    you can also use other virtual environment or use `pip install pypox` to install it directly to your current python environment. we recommend using `Python 3.11` and up for this system to work smoothly.

### Setting Up Your Project Structure

To begin using Pypox, create a folder named `src` where your project files will reside. Inside this folder, include the following files:

- `startup.py`
- `shutdown.py`
- `main.py`
- `config.py` (optional)

#### File Purposes:

- `startup.py` and `shutdown.py`: Handle the API's lifespan events.
- `main.py`: Acts as the entry point of your application when running with Uvicorn (`uvicorn src.main:app --reload` is an example command).
- `config.py` (optional): Used for configuring specific settings of your API.

### Initializing Pypox

Next, import Pypox in your `main.py` file and initialize it:

```python
from fastapi import FastAPI
from pypox import Pypox
import os

app: FastAPI = Pypox(os.path.dirname(__file__))()
```

This code automatically traverses your project directory, detecting the predefined conventions set by Pypox. It seamlessly includes them in the server, simplifying the process of serving your API.

### Serving it over ASGI Server

you can now use the command to serve it to http. for this example, we will use uvicorn

```bash
uvicorn src.main:app --reload
```

!!! note

    you can also use other **ASGI server** since **Pypox** is based on **FastAPI**. you can use other servers like. `Gunicorn`, `Hypercorn`, `Daphne`, etc. as long as the server complies to ASGI Specification.

### Tutorials

- [**Routing Tutorial**](/pypox/tutorials/routing/http/)

### Future Tutorials

Stay tuned for upcoming tutorials where you'll learn more about utilizing Pypox's conventions effectively. Please note that the documentation is a work in progress, and additional information will be added to help prepare your application for production.
