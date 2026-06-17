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

## Week 1 Day 3: Ingestion Design

Designed the ingestion layer for the engineering knowledge assistant.

### Key Decisions

- Raw files will first be converted into `RawDocument` objects.
- Documents will be parsed based on source type.
- Chunks will be source-aware instead of using one generic splitter.
- Design docs and incidents will use Markdown section-based chunking.
- Logs will use grouped event-based chunking.
- Code will initially use line-range chunking, with function-aware parsing planned later.
- Every chunk will carry metadata such as source type, path, component, tags, and related sources.

### Planned Ingestion Flow

```text
Raw files → RawDocument → Parsed sections/events/code blocks → ChunkDocument → JSONL output

## Week 1 Day 4: Basic Ingestion Pipeline

Implemented the first version of the ingestion pipeline.

### What It Does

- Loads raw files from design docs, logs, incidents, and selected Prometheus source directories.
- Converts each file into a `RawDocument`.
- Applies source-aware chunking.
- Converts each retrievable unit into a `ChunkDocument`.
- Writes ingestion artifacts to JSONL files.

### Chunking Strategies

| Source Type | Strategy |
|---|---|
| Design docs | Markdown section-based chunking |
| Incidents | Markdown section-based chunking |
| Logs | Grouped log lines |
| Code | Line-range chunks with overlap |

### Output Files

- `data/metadata/ingested_documents.jsonl`
- `data/metadata/chunks.jsonl`

### Why This Matters

The ingestion layer makes retrieval source-aware, metadata-rich, and citation-friendly. This avoids treating code, logs, incidents, and design documents as generic plain text.
