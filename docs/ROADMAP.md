<think>
Okay, I need to create a ROADMAP.md for the http-audit project. Let me start by understanding the current context. The tool is a Python script that provides real-time visibility into HTTP traffic at the kernel level. The user wants a roadmap with an MVP milestone, then v1 and v2 phases, each with themes. I should mark what's MVP-critical and be concrete and shippable.

First, the MVP. The MVP must include the core functionality that makes the tool usable. From the README, the main feature is real-time HTTP traffic visibility. So, the MVP should have kernel-level packet capture, real-time display of HTTP requests/responses, and maybe basic filtering. Also, the user needs to run the script with options, so command-line interface is essential. Logging to a file would be useful for later analysis. Security is important too, so running with minimal privileges and maybe a config file for settings.

Next, v1. After MVP, the next phase could focus on enhancing usability and adding features. A web-based dashboard would make it more accessible. Exporting data in formats like JSON or CSV would help with reporting. Alerting system for suspicious activity adds proactive monitoring. Integration with common tools like Wireshark or ELK stack would be valuable. Also, support for HTTPS inspection, but that requires handling SSL/TLS, which might need a separate tool or library.

For v2, the roadmap could expand to more advanced features. Distributed monitoring for multiple hosts, machine learning for anomaly detection, a plugin system for extensibility, and maybe a cloud version. These are more ambitious and can come after the core features are solid.

I need to make sure each phase builds on the previous one. MVP is the foundation, then v1 adds user-friendly features and integrations, v2 introduces scalability and advanced analysis. Also, check if there are any existing frameworks or tools mentioned in the company context that could be leveraged. The company uses vLLM and SGLang, but those are for inference and structured generation, so maybe not directly applicable here. The existing portfolio includes iceoryx2, which is an IPC library, but that's about communication between processes. The data sets available are for instruction-response pairs, which might not be directly relevant here.

Security considerations: the tool captures kernel-level traffic, so it needs to handle permissions carefully. The MVP should address running with minimal privileges. Also, HTTPS inspection in v1 would require handling SSL keys, which is a security concern. Need to mention that in the roadmap.

Testing and validation: the company's process includes QA and validation for willingness to pay. The roadmap should include testing phases, but since it's a roadmap, maybe focus on features rather than process steps. However, ensuring that each phase is shippable implies that testing is part of each milestone.

Documentation is important for each phase. The MVP should have basic usage docs, and later versions can expand with API docs, dashboard guides, etc.

Now, structure the markdown. Start with MVP, list critical features, then v1 and v2 with their themes. Use bullet points and mark MVP-critical items. Keep it professional and concise.
</think>

# ROADMAP.md

## MVP Milestone (Must-Have for Launch)
**Core Kernel-Level HTTP Visibility**
- ✅ **Kernel-level packet capture** (eBPF/XDP) for HTTP traffic interception  
- ✅ **Real-time CLI display** of HTTP requests/responses (headers, methods, status codes)  
- ✅ **Basic filtering** by IP, port, or HTTP method (CLI flags)  
- ✅ **Log output to file** (JSONL format) for post-analysis  
- ✅ **CLI interface** with `--help` documentation  
- ✅ **Privilege escalation mitigation** (drop root after capture setup)  
- ✅ **Configurable timeout** for session tracking  

## v1.0 Phase (6-8 weeks post-MVP)
**Theme: Enhanced Usability & Integration**  
- 📊 **Web-based dashboard** (React/Vue) for visualizing captured traffic  
- 🔄 **Export formats** (CSV, PCAP, JSON) for compatibility with analysis tools  
- 🔍 **Anomaly detection rules** (e.g., flag 500 errors, suspicious User-Agents)  
- 🔄 **API integration** for third-party tools (e.g., Slack alerts, Grafana dashboards)  
- 🔐 **HTTPS inspection** (with SSL key logging opt-in)  
- 🧪 **Unit/integration tests** (pytest coverage >80%)  
- 📚 **Developer documentation** (API reference, eBPF module architecture)  

## v2.0 Phase (3-4 months post-v1)
**Theme: Enterprise Scalability & Intelligence**  
- 🌐 **Distributed monitoring** (multi-host traffic aggregation via Kafka/Redis)  
- 🤖 **ML-based anomaly scoring** (integration with TensorFlow/PyTorch models)  
- 🔄 **Plugin system** (custom filters, exporters, and analyzers via Python hooks)  
- ☁️ **Cloud-native version** (Kubernetes operator + Helm charts)  
- 🛡️ **Audit compliance features** (HIPAA/GDPR metadata redaction, audit trails)  
- 🧰 **CLI subcommands** for advanced users (e.g., `http-audit replay`, `http-audit compare`)  
- 🧪 **Fuzz testing** for edge-case resilience  

*MVP-critical items marked with ✅. All phases include security hardening and performance benchmarks.*
