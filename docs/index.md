# Pypox

## Overview

The Pypox module is designed to dynamically generate a FastAPI application and API routers based on predefined conventions within a specified directory. It automatically discovers and integrates Python modules within the directory to create endpoints and configure API-related settings.

### Key Aspects

1. **Dynamic API Construction:** Pypox dynamically constructs APIs by inspecting the contents of modules within a specified directory. It follows a convention-based approach where modules adhering to predefined naming patterns are automatically integrated into the API structure.

2. **Convention-Driven Approach:** Modules within the designated directory must comply with specific naming conventions to be recognized and utilized by Pypox. These conventions define the purpose and functionality of each module, facilitating automatic endpoint creation and configuration.

3. **Flexibility and Extensibility:** While relying on conventions, Pypox provides flexibility in managing the API structure. Users can extend functionalities by adding modules that adhere to the prescribed naming conventions, enabling seamless integration into the API structure.

4. **Simplified Application Management:** Pypox handles various aspects of API construction, including route creation, endpoint configurations, and application lifecycle management. It streamlines the process of building FastAPI applications, reducing the need for manual configuration and setup.

5. **Lifespan Management:** The module supports the execution of startup and shutdown functions provided within modules. This feature enables proper initialization and cleanup routines, ensuring a well-managed application lifecycle.

### Use Cases

- **Rapid API Prototyping:** Pypox is particularly useful in scenarios requiring quick prototyping or development of RESTful APIs. By adopting a convention-driven approach, developers can focus more on implementing business logic and less on boilerplate code for setting up API endpoints.

- **Microservices Architecture:** In microservices-based architectures, where numerous services communicate via APIs, Pypox aids in standardizing API creation and configuration across multiple services. It promotes consistency in API development while allowing for individual service customization through conventions.

- **API Development Automation:** For projects involving frequent updates or additions to API endpoints, Pypox automates the process of integrating new endpoints or modifying existing ones. This feature helps in scaling applications without compromising on maintainability.

### Advantages

- **Reduced Development Time:** By automating API creation and configuration, Pypox significantly reduces the time spent on manual setup and management, accelerating the development cycle.

- **Consistency and Maintainability:** Enforcing naming conventions ensures a consistent API structure, simplifying maintenance and making the codebase more accessible to new developers.

- **Scalability and Adaptability:** Pypox's modular and convention-driven approach fosters scalability, allowing applications to grow while maintaining a coherent API structure.

- **Improved Collaboration:** The standardized approach to API development enhances collaboration among team members by establishing a common ground for understanding API endpoints and configurations.

## Features

- Automatic discovery of modules within a specified directory following specific file naming conventions.
- Dynamically generates FastAPI application and API routers based on discovered modules.
- Configures endpoints, their methods, and associated configurations based on module contents.
- Supports startup and shutdown functions to manage the application's lifespan.

## Installation

To use Pypox, you have multiple installation options:

### Using Pipenv

If you prefer managing dependencies within a virtual environment using Pipenv, you can install Pypox as follows:

```bash
pipenv install pypox
```

This command will create a Pipfile and Pipfile.lock and install Pypox along with its dependencies in a virtual environment managed by Pipenv.

### Using pip

Alternatively, you can install Pypox directly using pip:

```bash
pip install pypox
```

This command installs Pypox globally or within your current Python environment without creating a virtual environment.

### Usage

After installing Pypox, ensure the modules within the specified directory follow the naming conventions described in the documentation. Use Pypox by instantiating the `Pypox` class and generating the FastAPI application and API routers as demonstrated in the examples above.

## Uninstallation

To remove Pypox and its dependencies, you can use Pipenv or pip:

### Using Pipenv

```bash
pipenv uninstall pypox
```

This command removes Pypox from the Pipenv-managed virtual environment.

### Using pip

```bash
pip uninstall pypox
```

This command uninstalls Pypox globally or within your current Python environment.

## Usage

To use Pypox, follow these steps:

1. **Instantiate Pypox:** Create an instance of the `Pypox` class by providing a directory path containing modules following defined naming conventions.

   ```python
   pypox_instance = Pypox(directory_path)
   ```

2. **Invoke Pypox:** Call the `Pypox` instance as a function to generate the FastAPI application and API routers based on the discovered modules.

   ```python
   fastapi_app = pypox_instance()
   ```

3. **Run the FastAPI application:** Utilize the generated `FastAPI` instance to run the application.

   ```python
   import uvicorn

   if __name__ == "__main__":
       uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
   ```

## Dependencies

Pypox requires the following dependencies:

- `fastapi`
- `uvicorn[standard]`

## Limitations

- The module assumes specific file naming conventions for modules within the directory.
- It requires the presence of specific functions (`startup` and `shutdown`) for managing application lifespan.

```

```
