# Step 5: Write JSONL Outputs

import json
from dataclasses import asdict
from pathlib import Path

from .chunkers import chunk_document
from .loaders import load_documents
from .metadata import load_source_manifest


def write_jsonl(path: str, rows: list[dict]) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            
def run_ingestion(
    input_paths: list[str],
    manifest_path: str = "data/metadata/source_manifest.json",
    documents_output_path: str = "data/metadata/ingested_documents.jsonl",
    chunks_output_path: str = "data/metadata/chunks.jsonl",
    project_root: str = ".",
) -> None:
    manifest = load_source_manifest(manifest_path)

    documents = load_documents(
        input_paths=input_paths,
        manifest=manifest,
        project_root=project_root,
    )

    all_chunks = []
    for doc in documents:
        chunks = chunk_document(doc)
        all_chunks.extend(chunks)

    document_rows = []
    for doc in documents:
        document_rows.append(
            {
                "doc_id": doc.doc_id,
                "source_type": doc.source_type,
                "path": doc.path,
                "title": doc.title,
                "content_length": len(doc.content),
                "metadata": doc.metadata,
            }
        )

    chunk_rows = [asdict(chunk) for chunk in all_chunks]

    write_jsonl(documents_output_path, document_rows)
    write_jsonl(chunks_output_path, chunk_rows)

    print("Ingestion completed")
    print(f"Documents ingested: {len(documents)}")
    print(f"Chunks created: {len(all_chunks)}")
    print(f"Documents output: {documents_output_path}")
    print(f"Chunks output: {chunks_output_path}")
    
