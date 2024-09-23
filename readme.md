# DevOps API

## Overview
This application is featuring a Python-based REST API using Flask/FastAPI, PostgreSQL, and Prometheus for metrics. The API is fully Dockerized and Kubernetes-ready with the following features

## Features
- Resolve and validate IPv4 addresses for a given domain.
- Log and store queries in a PostgreSQL database.
- Metrics exposed for Prometheus.
- Kubernetes support via Helm Charts.

## Prerequisites
- Docker
- Docker Compose
- Helm (for Kubernetes)
- Redis (either running locally, in Docker, or in Kubernetes)

## Setup and Running Locally

### Using Docker Compose

1. Clone the repository:
    ```bash
    git clone git@github.com:jawadsiddiqui/devops-api.git
    cd devops-api
    ```

2. Build and start the services:
    ```bash
    docker-compose up -d --build
    ```

3. Access the API at `http://localhost:3000`.

4. To stop the services:
    ```bash
    docker-compose down
    ```

### Available Endpoints

- **Root**: `GET /` - Returns the current version, date (UNIX epoch), and Kubernetes status.
- **Health**: `GET /health` - Simple health check.
- **Metrics**: `GET /metrics` - Exposes Prometheus metrics.
- **IPv4 Lookup**: `POST /v1/tools/lookup` - Resolves the IPv4 address for a given domain.
- **IPv4 Validation**: `POST /v1/tools/validate` - Validates if an input is a valid IPv4 address.
- **Query History**: `GET /v1/history` - Retrieves the last 20 saved queries.

### Using Kubernetes with Helm

1. Install Helm:
    ```bash
    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
    ```

2. Deploy the application:
    ```bash
    helm install devops-api ./helm/devops-api
    ```

    If its already deployed then use below command to deploy latest helm

    ```bash
    helm upgrade devops-api ./helm/devops-api
    ```

## CI Pipeline

This project includes a GitHub Actions CI pipeline that:
- Runs tests and linting.
- Builds a Docker image.
- Packages the Helm chart.

You can view the pipeline in the `.github/workflows/ci.yml` file.

## Metrics and Monitoring

Prometheus metrics are exposed via `/metrics`. To monitor the application, set up Prometheus to scrape these metrics.
