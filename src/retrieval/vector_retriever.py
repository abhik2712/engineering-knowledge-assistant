# load FAISS index
# load vector chunk store
# embed query
# search FAISS
# map result indices back to chunks
# return RetrievalResult objects
# Example - 
# retriever.retrieve(
#     query="scrape timeout root cause",
#     top_k=5,
#     filters={"source_type": "incident"},
# )
# This means Search semantically, but only return incident chunks.
# Useful filters later:
#   {"source_type": "incident"}
#   {"source_type": "log"}
#   {"component": "scrape_manager"}
#   {"severity": "SEV-2"}

from typing import Any

from src.indexing.embedding_model import EmbeddingModel
from src.indexing.vector_index import load_chunk_store, load_faiss_index
from src.retrieval.models import RetrievalResult


class VectorRetriever:
    def __init__(
        self,
        index_path: str = "data/indexes/vector/faiss.index",
        chunk_store_path: str = "data/indexes/vector/chunk_store.jsonl",
        embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> None:
        self.index_path = index_path
        self.chunk_store_path = chunk_store_path
        self.embedding_model_name = embedding_model_name

        self.index = load_faiss_index(index_path)
        self.chunks = load_chunk_store(chunk_store_path)
        self.embedding_model = EmbeddingModel(model_name=embedding_model_name)

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[RetrievalResult]:
        query_embedding = self.embedding_model.embed_query(query)

        # Fetch more than top_k because we may apply filters afterward.
        search_k = min(max(top_k * 5, top_k), len(self.chunks))

        scores, indices = self.index.search(query_embedding, search_k)

        results: list[RetrievalResult] = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            chunk = self.chunks[idx]

            if filters and not self._matches_filters(chunk, filters):
                continue

            result = self._to_result(
                chunk=chunk,
                score=float(score),
                rank=len(results) + 1,
            )
            results.append(result)

            if len(results) >= top_k:
                break

        return results

    def _to_result(
        self,
        chunk: dict[str, Any],
        score: float,
        rank: int,
    ) -> RetrievalResult:
        return RetrievalResult(
            chunk_id=chunk["chunk_id"],
            doc_id=chunk["doc_id"],
            content=chunk["content"],
            score=score,
            rank=rank,
            retriever="vector",
            source_type=chunk["source_type"],
            path=chunk["path"],
            metadata=chunk.get("metadata", {}) or {},
        )

    def _matches_filters(
        self,
        chunk: dict[str, Any],
        filters: dict[str, Any],
    ) -> bool:
        metadata = chunk.get("metadata", {}) or {}

        for key, expected_value in filters.items():
            actual_value = chunk.get(key, metadata.get(key))

            if isinstance(expected_value, list):
                if actual_value not in expected_value:
                    return False
            else:
                if actual_value != expected_value:
                    return False

        return True