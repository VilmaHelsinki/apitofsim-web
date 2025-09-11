# Hello World Flask App

This is a minimal "Hello World" Flask application using `uv` for dependency management and Docker for containerization.

## Prerequisites

- Docker

## Running the Application

1.  **Build the Docker image:**

    ```bash
    docker build -t flask-hello-world .
    ```

2.  **Run the Docker container:**

    ```bash
    docker run -p 5000:5000 flask-hello-world
    ```

3.  **Access the application:**

    Open your web browser and navigate to [http://localhost:5000](http://localhost:5000).
