# Pypox Installation Guide

## Requirements

- Python (3.6 and above)

## Installation Steps

Pypox is a self-contained Python module and does not require specific installation steps. However, you can set it up using the following:

1. **Create a Virtual Environment (Optional but recommended):**

   ```bash
   python -m venv pypox_env
   source pypox_env/bin/activate  # For Linux/Mac
   ./pypox_env/Scripts/activate   # For Windows
   ```

2. **Install Pypox:**

   ```bash
   pip install pypox
   ```

3. **Usage:**

   - Ensure the modules within the specified directory follow the naming conventions described in the documentation.
   - Use Pypox by instantiating the `Pypox` class and generating the FastAPI application and API routers.

   Example:

   ```python
   from pypox import Pypox
   import uvicorn

   pypox_instance = Pypox("your_directory_path")
   fastapi_app = pypox_instance()

   if __name__ == "__main__":
       uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
   ```

## Uninstallation

To remove Pypox, simply run the command `pip uninstall pypox`

## Troubleshooting

- Ensure the modules follow the specified naming conventions to be recognized by Pypox.
- Check for any missing dependencies (`fastapi` and `uvicorn`).
- If encountering issues, refer to the documentation or create an issue in the repository.

For more detailed information, refer to the Pypox README or documentation.

If you encounter any problems or need further assistance, contact the maintainers via [karlalferezfx@gmail.com](mailto:karlalferezfx@gmail.com?subject=Issue%20with%20Pypox).
