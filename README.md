## Dataset

This project uses the open-source Prometheus repository as the primary code and documentation corpus. The dataset also includes synthetic logs, synthetic incident reports, and self-written mini design documents to simulate a realistic engineering knowledge base.

The synthetic files are intentionally created for RAG experimentation and do not represent real Prometheus production incidents.

### Data Sources

| Source | Path | Purpose |
|---|---|---|
| Prometheus source repo | `data/code_repo/prometheus` | Code and official documentation |
| Design docs | `data/design_docs` | Architecture-style explanations |
| Logs | `data/logs` | Debugging and operational failure examples |
| Incidents | `data/incidents` | Root cause, resolution, and postmortem data |

### Setup

Clone the Prometheus repository:

```bash
mkdir -p data/code_repo
git clone https://github.com/prometheus/prometheus.git data/code_repo/prometheus
