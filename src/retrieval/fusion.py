# It accepts multiple result lists:

# [
#   vector_results,
#   bm25_results
# ]

# Then:

# Deduplicates chunks by chunk_id
# Computes RRF score for each chunk
# Boosts chunks that appear in both retrievers
# Sorts by fused score
# Returns final RetrievalResult objects

from collections import defaultdict
from src.retrieval.models import RetrievalResult


def reciprocal_rank_fusion(
    result_lists: list[list[RetrievalResult]],
    top_k: int = 5,
    rrf_k: int = 60,
) -> list[RetrievalResult]:
    """
    Merge multiple ranked retrieval result lists using Reciprocal Rank Fusion.

    RRF score for a chunk:
        sum(1 / (rrf_k + rank)) across retrievers

    We deduplicate by chunk_id.
    """

    fused_scores: dict[str, float] = defaultdict(float)
    best_result_by_chunk_id: dict[str, RetrievalResult] = {}
    retriever_sources_by_chunk_id: dict[str, list[str]] = defaultdict(list)

    for results in result_lists:
        for result in results:
            fused_scores[result.chunk_id] += 1.0 / (rrf_k + result.rank)

            if result.chunk_id not in best_result_by_chunk_id:
                best_result_by_chunk_id[result.chunk_id] = result
            else:
                existing = best_result_by_chunk_id[result.chunk_id]

                # Keep the version with better rank for content/metadata display.
                if result.rank < existing.rank:
                    best_result_by_chunk_id[result.chunk_id] = result

            retriever_sources_by_chunk_id[result.chunk_id].append(result.retriever)

    ranked_chunk_ids = sorted(
        fused_scores.keys(),
        key=lambda chunk_id: fused_scores[chunk_id],
        reverse=True,
    )

    fused_results: list[RetrievalResult] = []

    for final_rank, chunk_id in enumerate(ranked_chunk_ids[:top_k], start=1):
        base_result = best_result_by_chunk_id[chunk_id]

        metadata = dict(base_result.metadata or {})
        metadata["fusion"] = {
            "method": "rrf",
            "rrf_score": fused_scores[chunk_id],
            "retrievers": sorted(set(retriever_sources_by_chunk_id[chunk_id])),
        }

        fused_results.append(
            RetrievalResult(
                chunk_id=base_result.chunk_id,
                doc_id=base_result.doc_id,
                content=base_result.content,
                score=fused_scores[chunk_id],
                rank=final_rank,
                retriever="hybrid_rrf",
                source_type=base_result.source_type,
                path=base_result.path,
                metadata=metadata,
            )
        )

    return fused_results