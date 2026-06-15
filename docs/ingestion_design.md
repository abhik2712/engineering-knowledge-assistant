# Ingestion Design

## Goal
The ingestion layer converts the raw engineering corpus into normalized document and chunk artifacts that can be consumed by indexing and retrieval components.

## Inputs
- `data/metadata/source_manifest.json`: declares the sources to ingest.
- `data/code_repo/prometheus`: primary code and documentation corpus.
- `data/design_docs`: self-written design references.
- `data/logs`: synthetic operational logs.
- `data/incidents`: synthetic incident reports.

## Outputs
- `data/metadata/ingested_documents.jsonl`: one normalized record per discovered file.
- `data/metadata/chunks.jsonl`: one or more retrieval-ready chunks per document.

## Module Layout
- `src/ingestion/loaders.py`: loads the manifest and discovers text files for each source.
- `src/ingestion/parsers.py`: derives titles, formats, and light cleanup such as front matter removal.
- `src/ingestion/metadata.py`: builds stable document and chunk identifiers plus common metadata fields.
- `src/ingestion/chunkers.py`: splits normalized documents into overlapping chunks.
- `src/ingestion/models.py`: dataclasses shared across the ingestion pipeline.
- `src/ingestion/pipeline.py`: orchestrates ingestion and writes JSONL artifacts.

## Pipeline Flow
1. Read the source manifest.
2. Enumerate files for each source, respecting include and exclude paths.
3. Load text content into raw document objects.
4. Normalize each document into a stable record with source-aware metadata.
5. Chunk document content with overlap to preserve local context.
6. Persist document and chunk artifacts to JSONL for downstream indexing.

## Design Choices
- Keep the first version file-based and deterministic so ingestion outputs are easy to inspect and diff.
- Store raw normalized content in the document artifact so later steps can be rerun without reparsing the original file.
- Use JSONL outputs because they stream well into vector indexing, keyword indexing, and offline evaluation jobs.
- Start with a simple character-window chunker, then upgrade to source-aware strategies for code, logs, and incidents as retrieval experiments mature.

## Expected Next Steps
- Add source-specific parsers for code symbols, log timestamps, and incident sections.
- Extend chunk metadata with tags like subsystem, incident id, language, and severity.
- Add a CLI entrypoint to run ingestion locally and in Docker.
- Introduce tests that snapshot small fixture corpora and validate deterministic chunk boundaries.
