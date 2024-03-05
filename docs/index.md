## Pypox 2.0.0

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/downloads/release/python-390/)

Pypox 2.0 is a lightweight and fast Python web framework built on top of Starlette. It aims to provide a flexible and modular development experience for web applications.

**Key Features:**

* **File-based routing:** Pypox leverages a file-based approach for defining application routes, making it intuitive and easy to manage.
* **Modular design:** The framework adopts a modular architecture, allowing developers to break down their applications into smaller, reusable components.
* **Processor-based functions:** Pypox introduces processor functions that handle request validation and transformation, simplifying the process of preparing data for your application logic.

**Advantages:**

* **Ease of use:** Pypox's file-based routing and modular design contribute to a user-friendly development experience, especially for beginners.
* **Performance:** Built upon Starlette, Pypox is known for its speed and efficiency, making it suitable for web applications requiring fast performance.
* **Flexibility:** The modular structure allows developers to customize their development process and integrate Pypox with other libraries and frameworks.

**Installation Guide:**

1. **Prerequisites:** Ensure you have Python 3.7 or above installed on your system. You can verify the installation by running `python --version` in your terminal.
2. **Install Pypox:** Use the pip package manager to install Pypox:

```bash
pip install pypox
```

**Usage Example:**

A basic Pypox application demonstrating a processing function:

```python

from pypox.processing.base import processor
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from pypox._types import QueryStr,QueryInt,BodyDict

app = Starlette()

@processor()
async def homepage(name:QueryStr,age:QueryInt,info:BodyDict) -> JSONResponse:
    return JSONResponse({"message": f"Hello, {name}! You are {age} years old. Info: {info}"})

app.add_route("/", homepage, methods=["GET"])

```

**Dependencies:**

* Python (>= 3.7)
* Starlette

**Limitations:**

* **Early stage:** As Pypox is still under development, it might have limited features or functionalities compared to more mature frameworks.
* **Documentation:** Comprehensive documentation might not be readily available yet, requiring developers to rely on source code and community resources for guidance.

**Further Resources:**

* PyPI page: [pypi pypox ON PyPI pypi.org]

This documentation overview provides a more comprehensive introduction to Pypox 2.0+. Remember that the framework is still under development, so keep an eye out for updates and refer to the official resources for the latest information.