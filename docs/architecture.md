# Architecture

## High-Level Architecture

```text
Engineering Sources
  ├── Prometheus codebase
  ├── Design docs
  ├── Synthetic logs
  └── Synthetic incident reports
        ↓
Ingestion Pipeline
        ↓
Source-Aware Chunking + Metadata Extraction
        ↓
Indexing Layer
  ├── Vector Index
  └── Keyword Index
        ↓
Query Router
        ↓
Hybrid Retriever
        ↓
Reranker
        ↓
Context Builder
        ↓
LLM Answer Generator
        ↓
Answer with Citations + Trace Logs
