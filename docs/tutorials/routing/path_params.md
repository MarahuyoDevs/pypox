In Pypox, you can create dynamic path parameters similar to FastAPI by utilizing folder naming conventions. Renaming a folder with brackets `[name]` indicates that it's a dynamic route. This dynamic route name can be directly used as a parameter within an endpoint function.

#### Defining Dynamic Paths

1. **Dynamic Route Structure:**

   - Rename a folder using brackets to signify it's a dynamic route.
     ```
     python_project/
     │
     └── routes/
         └── user/
             ├── [name]/
             │   └── get.py
             └── ...
     ```

2. **Creating Dynamic Endpoints:**
   - Utilize the dynamic route name as a parameter within the endpoint function.
     ```python
     # Example endpoint in /user/[name]/get.py
     async def endpoint(name: str):
         # Use 'name' parameter to access the dynamic path parameter value
         return {"message": f"Hello, {name}!"}
     ```

!!! danger

    Importing items within a dynamic route folder, such as schemas.py, poses a challenge due to Python's restriction on using brackets within import statements. This limitation only allows HTTP and WebSocket conventions to be utilized within this specific folder structure.

to solve this problem. simply import it beside the dynamic route folder.

```
python_project/
│
└── routes/
    └── user/
        ├── [name]/
        │   └── get.py
        └── schemas.py
```

this will work because it doesn't have any brackets in it. you can now use it in your module.

```python
from python_project.routes.user.schemas import MyPydanticTable
```

#### Accessing Path Parameters

- **Endpoint Implementation:**
  - Define endpoint functions within the corresponding dynamic path folder.
  - Use the parameter name identical to the dynamic route folder name (`[name]`) to access path parameter values.

This technique allows you to create flexible and dynamic endpoints in Pypox, enabling the extraction of path parameters directly from folder names within your route structure.
