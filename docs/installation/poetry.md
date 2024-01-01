### Pypox Poetry Installation Guide

#### Requirements

- Python (3.6 and above)

#### Installation Steps

Pypox is a self-contained Python module and can be easily set up using Poetry, following these steps:

1. **Create a Virtual Environment** (Optional but recommended):

   ```bash
   poetry init
   poetry shell
   ```

2. **Install Pypox**:

   ```bash
   poetry add pypox
   ```

#### Usage

Ensure the modules within the specified directory follow the naming conventions described in the documentation.

Use Pypox by instantiating the Pypox class and generating the FastAPI application and API routers.
Example:

```python
from pypox import Pypox
import uvicorn

pypox_instance = Pypox("your_directory_path")
fastapi_app = pypox_instance()

if __name__ == "__main__":
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
```

#### Uninstallation

To remove Pypox, simply run the command:

```bash
poetry remove pypox
```

#### Troubleshooting

- Ensure the modules follow the specified naming conventions to be recognized by Pypox.
- Check for any missing dependencies (fastapi and uvicorn).
- If encountering issues, refer to the documentation or create an issue in the repository.

For more detailed information, refer to the Pypox README or documentation.

For additional assistance, contact the maintainers via karlalferezfx@gmail.com.
