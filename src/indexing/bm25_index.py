# Build and save keyword index
import json
import pickle
import re
from pathlib import Path
from typing import Any

from rank_bm25 import BM25Okapi


def tokenize(text: str) -> list[str]:
    text = text.lower()

    # Keeps words, numbers, underscores, hyphens, and dots useful for logs/code.
    tokens = re.findall(r"[a-zA-Z0-9_\-\.]+", text)

    return tokens


def build_bm25_index(searchable_texts: list[str]) -> BM25Okapi:
    tokenized_corpus = [tokenize(text) for text in searchable_texts]
    return BM25Okapi(tokenized_corpus)


def save_bm25_index(index: BM25Okapi, output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("wb") as f:
        pickle.dump(index, f)


def load_bm25_index(index_path: str) -> BM25Okapi:
    path = Path(index_path)

    if not path.exists():
        raise FileNotFoundError(f"BM25 index not found: {index_path}")

    with path.open("rb") as f:
        return pickle.load(f)


def save_bm25_chunk_store(
    chunks: list[dict[str, Any]],
    searchable_texts: list[str],
    output_path: str,
) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        for chunk, searchable_text in zip(chunks, searchable_texts):
            row = {
                "chunk": chunk,
                "searchable_text": searchable_text,
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def load_bm25_chunk_store(chunk_store_path: str) -> list[dict[str, Any]]:
    path = Path(chunk_store_path)

    if not path.exists():
        raise FileNotFoundError(f"BM25 chunk store not found: {chunk_store_path}")

    rows = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))

    return rows