# TECH_SPEC.md – HTTP Audit Tool

---

## 1. Overview

The **HTTP Audit Tool** is a kernel‑level traffic observer that captures, parses, and stores HTTP traffic in real time. It is designed for security teams, compliance auditors, and network engineers who need a lightweight, low‑latency solution to monitor HTTP(S) traffic without the overhead of full packet capture or deep packet inspection.

Key characteristics:

| Feature | Description |
|---------|-------------|
| **Kernel‑level capture** | Uses eBPF programs attached to the `tc` (Traffic Control) hook to intercept packets before they reach user space. |
| **Real‑time visibility** | Parsed HTTP requests/responses are streamed to a user‑space collector and exposed via a REST API. |
| **Zero‑trust** | Runs in a privileged container with minimal host exposure; only the `/sys/fs/bpf` and `/proc` mounts are required. |
| **Extensible** | The collector can be extended with custom filters, anomaly detectors, or export hooks. |
| **Lightweight** | Minimal CPU and memory footprint – suitable for edge devices, CI pipelines, or production clusters. |

---

## 2. Architecture

```
+------------------+      +-------------------+      +-------------------+
|  Kernel (eBPF)   | ---> |  User‑Space       | ---> |  Storage / API    |
|  (tc hook)       |      |  Collector (Python) |      |  (FastAPI)        |
+------------------+      +-------------------+      +-------------------+
          ^                           |                         |
          |                           |                         |
          |                           v                         v
          |                    +-------------------+   +-------------------+
          |                    |  Optional UI      |   |  Optional Export  |
          |                    |  (React/Next.js)  |   |  (Kafka, S3, etc)|
          |                    +-------------------+   +-------------------+
```

### 2.1 Kernel Layer

* **eBPF Program** – Compiled from C source (`http_audit_kern.c`) using `clang` and loaded via `bcc`.  
* **Hook Point** – `tc` ingress/egress on the selected interface.  
* **Data Path** – Packets are filtered for TCP port 80/443, reassembled to HTTP payload, and a minimal context struct (`http_event_t`) is emitted to the user space via a perf ring buffer.

### 2.2 User‑Space Collector

* **Python Service** – `http_audit.py` orchestrates the eBPF loader, consumes events, parses HTTP, and persists them.  
* **Parser** – Handles both HTTP/1.1 and HTTP/2 (via `h2` library).  
* **Event Pipeline** –  
  1. **Ingress** – `bcc` perf buffer callback.  
  2. **Normalization** – Convert raw bytes to structured JSON.  
  3. **Enrichment** – Add timestamps, flow IDs, and optional geo‑IP.  
  4. **Persistence** – Write to a relational DB (PostgreSQL/SQLite).  
  5. **API Push** – Emit to FastAPI via in‑memory queue.

### 2.3 Storage & API Layer

* **Database** – PostgreSQL (production) or SQLite (dev).  
* **Schema** – `http_logs` table with indexes on `timestamp`, `src_ip`, `dst_ip`, `method`, `status`.  
* **REST API** – FastAPI exposes endpoints for querying logs, aggregations, and alerts.  
* **Export Hooks** – Optional Kafka producer or S3 uploader for downstream analytics.

---

## 3. Components

| Component | Responsibility | Language / Tool |
|-----------|----------------|-----------------|
| `http_audit_kern.c` | eBPF program | C |
| `http_audit.py` | Orchestrator, collector, parser | Python 3.10+ |
| `api.py` | FastAPI server | Python |
| `models.py` | SQLAlchemy ORM | Python |
| `Dockerfile` | Container build | Docker |
| `docker-compose.yml` | Multi‑service orchestration | Docker Compose |
| `requirements.txt` | Python dependencies | pip |
| `Makefile` | Build & run helpers | Make |

---

## 4. Data Model

```sql
CREATE TABLE http_logs (
    id              BIGSERIAL PRIMARY KEY,
    timestamp       TIMESTAMP WITH TIME ZONE NOT NULL,
    src_ip          INET NOT NULL,
    src_port        SMALLINT NOT NULL,
    dst_ip          INET NOT NULL,
    dst_port        SMALLINT NOT NULL,
    method          TEXT,
    url             TEXT,
    http_version    TEXT,
    status_code     SMALLINT,
    request_headers JSONB,
    response_headers JSONB,
    request_body    BYTEA,
    response_body   BYTEA,
    latency_ms      INTEGER,
    flow_id         TEXT,
    tags            TEXT[]
);
