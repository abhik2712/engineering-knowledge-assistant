import numpy as np

from src.indexing.bm25_index import (
    load_bm25_chunk_store,
    load_bm25_index,
    tokenize,
)
from src.indexing.embedding_model import EmbeddingModel
from src.indexing.vector_index import load_chunk_store, load_faiss_index


VECTOR_INDEX_PATH = "data/indexes/vector/faiss.index"
VECTOR_CHUNK_STORE_PATH = "data/indexes/vector/chunk_store.jsonl"

BM25_INDEX_PATH = "data/indexes/bm25/bm25.pkl"
BM25_CHUNK_STORE_PATH = "data/indexes/bm25/chunk_store.jsonl"


def print_result(rank: int, score: float, chunk: dict) -> None:
    metadata = chunk.get("metadata", {}) or {}

    print("=" * 100)
    print(f"Rank: {rank}")
    print(f"Score: {score:.4f}")
    print(f"Chunk ID: {chunk.get('chunk_id')}")
    print(f"Source Type: {chunk.get('source_type')}")
    print(f"Path: {chunk.get('path')}")

    if metadata.get("section"):
        print(f"Section: {metadata.get('section')}")

    if metadata.get("component"):
        print(f"Component: {metadata.get('component')}")

    if metadata.get("severity"):
        print(f"Severity: {metadata.get('severity')}")

    preview = chunk.get("content", "")[:600].replace("\n", " ")
    print(f"Preview: {preview}")


def search_vector(query: str, top_k: int = 5) -> None:
    print("\n\nVECTOR SEARCH")
    print(f"Query: {query}")

    index = load_faiss_index(VECTOR_INDEX_PATH)
    chunks = load_chunk_store(VECTOR_CHUNK_STORE_PATH)

    embedding_model = EmbeddingModel()
    query_embedding = embedding_model.embed_query(query)

    scores, indices = index.search(query_embedding, top_k)

    for rank, (score, idx) in enumerate(zip(scores[0], indices[0]), start=1):
        if idx == -1:
            continue
        print_result(rank, float(score), chunks[idx])


def search_bm25(query: str, top_k: int = 5) -> None:
    print("\n\nBM25 SEARCH")
    print(f"Query: {query}")

    bm25 = load_bm25_index(BM25_INDEX_PATH)
    rows = load_bm25_chunk_store(BM25_CHUNK_STORE_PATH)

    tokenized_query = tokenize(query)
    scores = bm25.get_scores(tokenized_query)

    top_indices = np.argsort(scores)[::-1][:top_k]

    for rank, idx in enumerate(top_indices, start=1):
        row = rows[idx]
        chunk = row["chunk"]
        score = float(scores[idx])
        print_result(rank, score, chunk)


def main() -> None:
    queries = [
        "Why are targets becoming unhealthy during scraping?",
        "context deadline exceeded",
        "What caused INC-003?",
        "Explain remote write backpressure",
        "Which component handles alert rule evaluation?",
    ]

    for query in queries:
        search_vector(query, top_k=5)
        search_bm25(query, top_k=5)


if __name__ == "__main__":
    main()