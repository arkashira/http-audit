# REQUIREMENTS.md

## Project Overview
**Project**: `http-audit`  
**Purpose**: Provide real‑time visibility into HTTP traffic at the kernel level, enabling security teams, developers, and compliance auditors to monitor, analyze, and respond to HTTP traffic patterns without the overhead of traditional packet sniffers.

---

## 1. Functional Requirements

| ID   | Requirement | Description | Acceptance Criteria |
|------|-------------|-------------|---------------------|
| **FR‑1** | Kernel‑level HTTP capture | Capture all HTTP(S) traffic (TCP ports 80, 443, and any user‑specified ports) directly from the kernel using eBPF or equivalent. | • Captured packets are available to user space within < 5 ms of arrival.<br>• No packets are dropped under normal load. |
| **FR‑2** | Request/Response parsing | Parse captured packets into structured HTTP request/response objects, including headers, body, status codes, and TLS metadata. | • Parsed objects match RFC 7230/7231 specifications.<br>• Binary bodies are base64‑encoded for safe storage. |
| **FR‑3** | Filtering & whitelisting | Allow users to filter traffic by IP, port, method, URL pattern, or header values via CLI flags or a config file. | • Filters are applied before logging; non‑matching traffic is discarded. |
| **FR‑4** | Real‑time dashboard | Provide a lightweight web UI (served on localhost) that displays live traffic summaries, top endpoints, and latency histograms. | • Dashboard refreshes every 2 s.<br>• UI is responsive on modern browsers. |
| **FR‑5** | Export & persistence | Persist captured data to disk in JSON Lines format and optionally stream to a remote syslog or Kafka endpoint. | • Exported file size ≤ 1 GB per hour on average traffic.<br>• Remote stream uses TLS 1.2+. |
| **FR‑6** | CLI interface | Expose a command‑line interface with sub‑commands: `start`, `stop`, `status`, `config`. | • `http_audit.py start --help` shows all options. |
| **FR‑7** | Graceful shutdown | On SIGINT/SIGTERM, flush buffers, close sockets, and terminate eBPF programs cleanly. | • No data loss on shutdown; exit code 0. |
| **FR‑8** | Logging & diagnostics | Log internal state, errors, and performance metrics to a separate log file. | • Log rotation every 10 MB, keep 5 backups. |
| **FR‑9** | Extensibility hooks | Provide a plugin API for custom parsers or exporters. | • Plugin can be loaded via a `--plugin` flag. |
| **FR‑10** | Security controls | Enforce that only privileged users can run the tool; prevent privilege escalation via eBPF. | • Tool refuses to start if not run as root or with CAP_SYS_ADMIN. |

---

## 2. Non‑Functional Requirements

| ID   | Requirement | Description | Acceptance Criteria |
|------|-------------|-------------|---------------------|
| **NFR‑1** | Performance | Capture throughput ≥ 10 000 HTTP requests per second on a 2 GHz CPU with < 10 % CPU usage. | • Benchmark on a 4‑core VM shows CPU < 10 % under load. |
| **NFR‑2** | Latency | End‑to‑end processing (capture → parse → log) < 10 ms per request. | • Latency measured via synthetic traffic. |
| **NFR‑3** | Reliability | 99.9 % uptime over a 30‑day period. | • Automated health checks report status every 30 s. |
| **NFR‑4** | Security | Data stored on disk must be encrypted at rest (AES‑256). | • File system permissions restrict access to owner only. |
| **NFR‑5** | Compatibility | Works on Linux kernel ≥ 5.8, Python 3.10+. | • CI tests run on Ubuntu 22.04 and CentOS Stream 9. |
| **NFR‑6** | Usability | CLI and UI documentation available via `--help` and `/docs`. | • `http_audit.py --help` shows all options; UI has inline tooltips. |
| **NFR‑7** | Maintainability | Code follows PEP 8, uses type hints, and has 80 %+ test coverage. | • CI pipeline enforces linting and coverage thresholds. |
| **NFR‑8** | Extensibility | New protocols (e.g., QUIC) can be added via plugins without core changes. | • Plugin example demonstrates adding QUIC support. |

---

## 3. Constraints

| ID   | Constraint | Description |
|------|------------|-------------|
| **C‑1** | Root privileges | Tool must run as root or with CAP_SYS_ADMIN; cannot be sandboxed in unprivileged containers. |
| **C‑2** | eBPF support | Requires kernel with eBPF support; older kernels (≤ 4.15) are unsupported. |
| **C‑3** | Disk space | Exported logs may consume significant disk space; users must provision at least 10 GB per day. |
| **C‑4** | External dependencies | Must not rely
