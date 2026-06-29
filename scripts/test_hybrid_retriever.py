from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.hybrid_retriever import HybridRetriever
from src.retrieval.retrieval_debugger import print_results
from src.retrieval.vector_retriever import VectorRetriever


def main() -> None:
    vector_retriever = VectorRetriever()
    bm25_retriever = BM25Retriever()

    hybrid_retriever = HybridRetriever(
        vector_retriever=vector_retriever,
        bm25_retriever=bm25_retriever,
        rrf_k=60,
    )

    queries = [
        "Why are targets becoming unhealthy during scraping?",
        "context deadline exceeded",
        "What caused INC-003?",
        "Explain remote write backpressure",
        "Which component handles alert rule evaluation?",
    ]

    for query in queries:
        vector_results = vector_retriever.retrieve(query=query, top_k=5)
        bm25_results = bm25_retriever.retrieve(query=query, top_k=5)
        hybrid_results = hybrid_retriever.retrieve(
            query=query,
            top_k=5,
            candidate_k=20,
        )

        print_results(
            query=query,
            results=vector_results,
            title="VECTOR RESULTS",
        )

        print_results(
            query=query,
            results=bm25_results,
            title="BM25 RESULTS",
        )

        print_results(
            query=query,
            results=hybrid_results,
            title="HYBRID RRF RESULTS",
        )


if __name__ == "__main__":
    main()