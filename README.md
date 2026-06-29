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
```
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
```
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

## Week 1 Day 5: Indexing Design

Designed the indexing layer for the RAG system.

### Index Types

The system will use two retrieval indexes:

| Index | Purpose |
|---|---|
| Vector index | Semantic retrieval |
| BM25 index | Keyword and exact-match retrieval |

### Embedding Model

Initial embedding model:

`sentence-transformers/all-MiniLM-L6-v2`

This model is lightweight, local, and sufficient for a first retrieval baseline.

### Indexing Flow

```text
chunks.jsonl
  → embedding text construction
  → vector embeddings
  → FAISS index
  → BM25 index
```

## Week 1 Day 6: Indexing Implementation

Implemented the first indexing layer for the engineering knowledge assistant.

### Implemented Indexes

| Index | Purpose |
|---|---|
| FAISS vector index | Semantic retrieval |
| BM25 index | Keyword and exact-match retrieval |

### Input

- `data/metadata/chunks.jsonl`

### Outputs

- `data/indexes/vector/faiss.index`
- `data/indexes/vector/chunk_store.jsonl`
- `data/indexes/bm25/bm25.pkl`
- `data/indexes/bm25/chunk_store.jsonl`

### Key Design Choice

Each chunk is converted into metadata-aware searchable text before indexing. This improves retrieval by including source type, component, section, severity, tags, path, and content.

### Manual Test Queries

- Why are targets becoming unhealthy during scraping?
- context deadline exceeded
- What caused INC-003?
- Explain remote write backpressure
- Which component handles alert rule evaluation?

## Week 1 Day 7: Basic Retriever Layer

Implemented the first retrieval layer over the indexed corpus.

### Implemented Retrievers

| Retriever | Purpose |
|---|---|
| VectorRetriever | Semantic search over FAISS index |
| BM25Retriever | Keyword and exact-match search over BM25 index |

### Common Result Model

Both retrievers return a common `RetrievalResult` object containing:

- chunk_id
- doc_id
- content
- score
- rank
- retriever name
- source_type
- path
- metadata

### Filtering Support

Retrievers support metadata-aware filtering, for example:

```python
filters={"source_type": "incident"}
filters={"component": "scrape_manager"}
```

## Week 2 Day 8: Hybrid Retrieval with RRF

Implemented hybrid retrieval by combining vector search and BM25 search using Reciprocal Rank Fusion.

### Why Hybrid Retrieval?

Vector search handles semantic queries, while BM25 handles exact matches such as:

- incident IDs
- error messages
- component names
- code symbols
- config keys

Combining both improves recall and robustness for engineering questions.

### Implemented Components

- `VectorRetriever`
- `BM25Retriever`
- `reciprocal_rank_fusion`
- `HybridRetriever`

### Retrieval Flow

```text
User query
  → VectorRetriever top-k
  → BM25Retriever top-k
  → RRF fusion
  → final top-k chunks
```

