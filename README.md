# Car App for Testing

## Environment Setup

**Don't forget to set the environment variables in the `.env` file.**

## Local Development

To start the application locally, follow these steps:

1. Install dependencies:

    ```bash
    poetry install
    ```

2. Activate the virtual environment:

    ```bash
    poetry shell
    ```

3. Start the FastAPI application:

    ```bash
    uvicorn app.main:app
    ```

## Docker Setup

To start the Docker container with the database:

1. Build the Docker image:

    ```bash
    sudo docker-compose build
    ```

    *Or, to build without using the cache:*

    ```bash
    sudo docker-compose build --no-cache
    ```

2. Start the containers in detached mode:

    ```bash
    sudo docker-compose up -d
    ```

## Running Tests

To run tests:

1. First, install dependencies:

    ```bash
    poetry install
    ```

2. Run the tests using `pytest`:

    ```bash
    poetry run pytest
    ```

## Running Migrations

To run database migrations with Alembic:

1. First, install dependencies:

    ```bash
    poetry install
    ```

2. Apply the migrations:

    ```bash
    alembic upgrade head
    ```
