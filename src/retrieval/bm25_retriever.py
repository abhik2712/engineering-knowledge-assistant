# load BM25 index
# load BM25 chunk store
# tokenize query
# score all chunks
# sort by score
# return top-k RetrievalResult objects

from typing import Any

import numpy as np

from src.indexing.bm25_index import (
    load_bm25_chunk_store,
    load_bm25_index,
    tokenize,
)
from src.retrieval.models import RetrievalResult


class BM25Retriever:
    def __init__(
        self,
        index_path: str = "data/indexes/bm25/bm25.pkl",
        chunk_store_path: str = "data/indexes/bm25/chunk_store.jsonl",
    ) -> None:
        self.index_path = index_path
        self.chunk_store_path = chunk_store_path

        self.index = load_bm25_index(index_path)
        self.rows = load_bm25_chunk_store(chunk_store_path)

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[RetrievalResult]:
        tokenized_query = tokenize(query)

        if not tokenized_query:
            return []

        scores = self.index.get_scores(tokenized_query)
        sorted_indices = np.argsort(scores)[::-1]

        results: list[RetrievalResult] = []

        for idx in sorted_indices:
            score = float(scores[idx])

            # Ignore zero-score BM25 matches.
            if score <= 0:
                continue

            row = self.rows[idx]
            chunk = row["chunk"]

            if filters and not self._matches_filters(chunk, filters):
                continue

            result = self._to_result(
                chunk=chunk,
                score=score,
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
            retriever="bm25",
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