Pypox utilizes its own convention for handling application startup and shutdown events, managed by `startup.py` and `shutdown.py`. These files contain an `async __call__` function, which Pypox recognizes as valid lifespans.

#### Setting Up Startup and Shutdown Events

1. **Startup Events (startup.py):**
   In the `startup.py` file, define the `async __call__` function to manage startup events. For instance:

   ```python
   async def __call__(app: FastAPI):
       print("System starting up")
   ```

2. **Shutdown Events (shutdown.py):**
   Similarly, within the `shutdown.py` file, create the `async __call__` function to handle shutdown events. For example:

   ```python
   async def __call__(app: FastAPI):
       print("Shutting down the system.")
   ```

#### Integrating Lifespan Events

These lifespan events can perform various tasks such as initializing connections, cleaning up resources, or performing setup/teardown operations. In your Pypox application, these files can be used for tasks like database initialization or cleanup.

Additionally, these lifespan events can be linked to other functionalities within your Pypox application for a seamless integration experience. If you're interested in integrating databases, check out the [Database Integration Tutorial](/pypox/tutorials/database) for a comprehensive guide on leveraging databases within your Pypox application.
