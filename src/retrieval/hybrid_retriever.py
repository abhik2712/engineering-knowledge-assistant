from typing import Any

from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.fusion import reciprocal_rank_fusion
from src.retrieval.models import RetrievalResult
from src.retrieval.vector_retriever import VectorRetriever


class HybridRetriever:
    def __init__(
        self,
        vector_retriever: VectorRetriever | None = None,
        bm25_retriever: BM25Retriever | None = None,
        rrf_k: int = 60,
    ) -> None:
        self.vector_retriever = vector_retriever or VectorRetriever()
        self.bm25_retriever = bm25_retriever or BM25Retriever()
        self.rrf_k = rrf_k

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        candidate_k: int = 20,
        filters: dict[str, Any] | None = None,
    ) -> list[RetrievalResult]:
        """
        Retrieve from vector and BM25, then merge using RRF.

        top_k:
            Final number of chunks returned.

        candidate_k:
            Number of candidates fetched from each retriever before fusion.
            Usually candidate_k > top_k.
        """
        
        # Why candidate_k is bigger than top_k
        # If final top_k = 5, do not fetch only 5 from each retriever.
        # Fetch more candidates:
        # Vector top 20
        # BM25 top 20
        # ↓
        # RRF
        # ↓
        # Final top 5
        # Why?
        # Because a result ranked 8 in vector and 7 in BM25 may be better overall than a result ranked 3 in only one retriever.

        vector_results = self.vector_retriever.retrieve(
            query=query,
            top_k=candidate_k,
            filters=filters,
        )

        bm25_results = self.bm25_retriever.retrieve(
            query=query,
            top_k=candidate_k,
            filters=filters,
        )

        fused_results = reciprocal_rank_fusion(
            result_lists=[vector_results, bm25_results],
            top_k=top_k,
            rrf_k=self.rrf_k,
        )

        return fused_results