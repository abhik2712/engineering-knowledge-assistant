# Build and save FAISS vector index.
import json
from pathlib import Path
from typing import Any

import faiss
import numpy as np


def build_faiss_index(embeddings: np.ndarray) -> faiss.Index:
    if embeddings.ndim != 2:
        raise ValueError("Embeddings must be a 2D numpy array")

    dimension = embeddings.shape[1]

    # Since embeddings are normalized, inner product behaves like cosine similarity.
    # index is a pointer to faiss.IndexFlatIP which is a flat (non-compressed) index that uses inner product for similarity search.
    # index points to the memory address which stores the embeddings and allows for efficient similarity search.
    # memory Layout: 
    # index (Pointer) ──> [ FAISS IndexFlatL2 Object ]
    #                  │  - d = 384
    #                  │  - ntotal = 2
    #                  │  - xb (Internal Pointer) ──> ┌────────────────────────────────────────┐
    #                                                │ Address 0x001: [ 384 float32 values ]  │ <── Vector 0
    #                                                ├────────────────────────────────────────┤
    #                                                │ Address 0x601: [ 384 float32 values ]  │ <── Vector 1
    #                                                └────────────────────────────────────────┘
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    return index


def save_faiss_index(index: faiss.Index, output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(path))


def load_faiss_index(index_path: str) -> faiss.Index:
    path = Path(index_path)

    if not path.exists():
        raise FileNotFoundError(f"FAISS index not found: {index_path}")

    return faiss.read_index(str(path))


def save_chunk_store(chunks: list[dict[str, Any]], output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")


def load_chunk_store(chunk_store_path: str) -> list[dict[str, Any]]:
    path = Path(chunk_store_path)

    if not path.exists():
        raise FileNotFoundError(f"Chunk store not found: {chunk_store_path}")

    chunks = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line))

    return chunks