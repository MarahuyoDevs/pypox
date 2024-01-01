Pypox provides configuration management via `config.py`, enabling adjustment of OpenAPI Specification (OAS) values. You can employ `config.py` at different project levels, affecting the main application or specific routes.

#### Top-Level Configuration (main.py)

1. **Project Structure Example:**
   Consider the following structure for top-level configuration:

   ```
   python_project/
   │
   ├── main.py
   └── config.py
   ```

2. **Utilizing `config.py`:**
   - **`config.py` at the Top Level:**  
     Define primary OAS specifications like title, license, contact, etc., within `config.py` to affect the entire application.

#### Route-Specific Configuration

1. **Project Structure Example:**
   For route-specific configurations, organize your project structure as follows:

   ```
   python_project/
   │
   └── routes/
       └── user/
           ├── config.py
           ├── get.py
           └── post.py
           └── ...
   ```

`config.py`

```python
title = "My sample application"
summary = "very simple application"
# rest of the configuration goes here
...
```

**Using `config.py` within a Route:**

**`config.py` Inside the Route Folder:**  
In this scenario, you can adjust route-specific OAS variables like tags, schemas, etc., by placing a `config.py` file inside the respective route folder. This allows tailored OAS configurations for individual routes.

`routes/user/config.py`

```python
tags = ["User information route."]
# rest of the configuration goes here
...
```

#### Implementation Guidelines

- **Main Application Configuration:**
  - Use top-level `config.py` to define global OAS settings for the entire application.
- **Route-Specific Configuration:**
  - Leverage route-specific `config.py` files within route folders to customize OAS parameters exclusively for those routes.

Utilize these configuration options to fine-tune your OAS specifications based on the scope of your Pypox application.
