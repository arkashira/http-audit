# tech-spec.md

## Stack
- **Language**: Go
- **Framework**: Gin (for HTTP server)
- **Runtime**: Linux Kernel (with eBPF for auditing)

## Hosting
- **Free Tier**: Yes (limited features for basic monitoring)
- **Specific Platforms**:
  - AWS EC2
  - Google Cloud Compute Engine
  - DigitalOcean Droplets
  - Self-hosted on any Linux distribution

## Data Model
### Tables/Collections
1. **AuditLogs**
   - **Key Fields**:
     - `id`: UUID (Primary Key)
     - `timestamp`: DATETIME
     - `http_method`: VARCHAR(10)
     - `url`: VARCHAR(255)
     - `response_code`: INT
     - `response_time`: FLOAT
     - `client_ip`: VARCHAR(45)
     - `user_agent`: VARCHAR(255)

2. **Anomalies**
   - **Key Fields**:
     - `id`: UUID (Primary Key)
     - `log_id`: UUID (Foreign Key referencing AuditLogs)
     - `anomaly_type`: VARCHAR(50)
     - `description`: TEXT
     - `timestamp`: DATETIME

## API Surface
1. **GET /api/v1/audit-logs**
   - **Purpose**: Retrieve a list of audit logs.
  
2. **POST /api/v1/audit-logs**
   - **Purpose**: Submit a new audit log entry.

3. **GET /api/v1/anomalies**
   - **Purpose**: Retrieve a list of detected anomalies.

4. **POST /api/v1/anomalies**
   - **Purpose**: Submit a new anomaly detection result.

5. **GET /api/v1/config**
   - **Purpose**: Retrieve current configuration settings.

6. **PUT /api/v1/config**
   - **Purpose**: Update configuration settings.

7. **GET /api/v1/health**
   - **Purpose**: Check the health status of the service.

8. **POST /api/v1/alerts**
   - **Purpose**: Create a new alert based on specific criteria.

## Security Model
- **Authentication**: OAuth 2.0 for API access.
- **Secrets Management**: Use AWS Secrets Manager or HashiCorp Vault for storing sensitive information.
- **IAM**: Role-based access control (RBAC) to manage permissions for different user roles.

## Observability
- **Logs**: 
  - Centralized logging with ELK Stack (Elasticsearch, Logstash, Kibana).
  - Structured logging in JSON format.

- **Metrics**: 
  - Prometheus for collecting and storing metrics.
  - Key metrics include request counts, response times, error rates.

- **Traces**: 
  - OpenTelemetry for distributed tracing.
  - Trace HTTP requests through the system to identify bottlenecks.

## Build/CI
- **Version Control**: Git (GitHub repository).
- **CI/CD Pipeline**: 
  - GitHub Actions for continuous integration and deployment.
  - Automated tests for unit, integration, and end-to-end testing.
- **Containerization**: Docker for packaging the application.
- **Deployment**: Kubernetes for orchestration and scaling.