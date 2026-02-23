# `.env` File

A `.env` is a **environment file**, a plain text file commonly used in software development projects. It serves as a configuration file that stores environment variables.

!!! info "Info!"
    Environment variables are key-value pairs that hold **sensitive** or environment-specific information, such as:
        
    - API keys
    - Access tokens
    - Database credentials
    - Other configuration settings.

The `.env` file plays a crucial role in separating sensitive or environment-specific data from the source code.

By storing such information in a separate file, developers can easily manage different configurations for various environments (e.g., development, staging, production) **without modifying the codebase**.

!!! tip "Tip!"
    Stop hardcoding configuration values in source code.
    
    Use `.env` instead!

This approach **enhances security** and simplifies the deployment process.

!!! danger "Never commit!"
    `.env` files must remain outside of version control systems (e.g., github, gitlab, bitbucket), preventing accidental exposure!

    Configure `.gitignore` appropriately.

## Dot Example!

It is recommended to create an `.env.example` file, this must be **committed in the repository**. It must contain **all the environment variables** necessary to start the application or model, but with **dummy values**.

This way, whoever is going to deploy the ML application, will know what to configure so that the application starts successfully!

A `.env.example` file:
```console
DB_HOST="1.2.3.4"
DB_PORT=1122
DB_USERNAME="some_username"
DB_PASSWORD=abc123
DB_DATABASE="some_db"
GITHUB_TOKEN_ACCESS="ghp_123412341234123412341234123412341234"
```

## Reading `.env`

Install de lib:

<div class="termy">

    ```console
    $ pip install python-dotenv
    ```

</div>

<br>
So environment variables can be read in Python with:

```python
import os
from dotenv import load_dotenv

# Reading .env and creating environment variables
load_dotenv()

# Reading environment variable
host = os.getenv("DB_HOST")

# Using environment variable
print(host)
```