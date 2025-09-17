# Hello World Quart App

This is a minimal "Hello World" Quart application using `uv` for dependency management and Docker for containerization.

## Prerequisites

- Docker
- uv (for local development)

## Running the Application with Docker

1.  **Build the Docker image:**

    ```bash
    docker build -t quart-hello-world .
    ```

2.  **Run the Docker container:**

    ```bash
    docker run -p 5000:5000 quart-hello-world
    ```

3.  **Access the application:**

    Open your web browser and navigate to [http://localhost:5000](http://localhost:5000).

## Running the Application Locally with uv

1.  **Install dependencies:**

    ```bash
    uv sync
    ```

2.  **Run the application:**

    ```bash
    CHAINS=config_list.json uv run quart --app vms run --debug
    ```

3.  **Access the application:**

    Open your web browser and navigate to [http://localhost:5000](http://localhost:5000).
