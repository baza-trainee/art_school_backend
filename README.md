![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Docker-compose](https://img.shields.io/badge/docker-compose-orange.svg)](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04)
![Linux (Ubuntu)](https://img.shields.io/badge/linux-ubuntu-green.svg)
## Installation

To run the project, you will need [Docker-compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04) installed. Follow these steps to install and run the project:

1. Create a new folder for your project.

2. Open the project in an IDE

3. Initialize Git

    ```
    git init
    ```
4. Add the remote repository
    ```
    git remote add origin https://github.com/baza-trainee/art_school_backend.git
    ```
5. Sync with the remote repository

    ```
    git pull origin dev
    ```
6. Create a `.env` file if it does not already exist and set the necessary environment variables:

    ```
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=school_db
    DB_USER=admin
    DB_PASS=admin

    POSTGRES_DB=school_db
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=admin
    ```

7. Initialize and start the containers:

    ```
    make run
    ```



[FastAPI-badge]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi

[FastAPI-url]: https://fastapi.tiangolo.com/

[FastAPIUsers-badge]: https://img.shields.io/badge/FastAPI%20Users-ef5552?style=for-the-badge

[FastAPIUsers-url]: https://fastapi-users.github.io/fastapi-users

[SQLAlchemy-badge]: https://img.shields.io/badge/sqlalchemy-fbfbfb?style=for-the-badge

[SQLAlchemy-url]: https://www.sqlalchemy.org/