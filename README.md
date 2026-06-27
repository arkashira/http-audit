# http-audit

A Python project for auditing HTTP events.

## Quick Start

1. Build the Docker image: `docker build -t http-audit .`
2. Run the Docker container: `docker run -p 8080:8080 http-audit`
3. Access the HTTP audit dashboard: `http://localhost:8080`

## Helm Chart

1. Install the Helm chart: `helm install http-audit`
2. Access the HTTP audit dashboard: `http://http-audit:8080`

## CI Pipeline

1. Run the CI pipeline: `make ci`
2. Verify the unit and integration tests pass
