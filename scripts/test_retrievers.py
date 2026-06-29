from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.retrieval_debugger import print_results
from src.retrieval.vector_retriever import VectorRetriever


def main() -> None:
    vector_retriever = VectorRetriever()
    bm25_retriever = BM25Retriever()
    
    query = "scrape timeout root cause"

    incident_results = vector_retriever.retrieve(
        query=query,
        top_k=5,
        filters={"source_type": "incident"},
    )

    log_results = bm25_retriever.retrieve(
        query="context deadline exceeded",
        top_k=5,
        filters={"source_type": "log"},
    )

    print_results(
        query=query,
        results=incident_results,
        title="VECTOR INCIDENT-ONLY RESULTS",
    )

    print_results(
        query="context deadline exceeded",
        results=log_results,
        title="BM25 LOG-ONLY RESULTS",
    )

    # queries = [
    #     "Why are targets becoming unhealthy during scraping?",
    #     "context deadline exceeded",
    #     "What caused INC-003?",
    #     "Explain remote write backpressure",
    #     "Which component handles alert rule evaluation?",
    # ]

    # for query in queries:
    #     vector_results = vector_retriever.retrieve(query=query, top_k=5)
    #     bm25_results = bm25_retriever.retrieve(query=query, top_k=5)

    #     print_results(
    #         query=query,
    #         results=vector_results,
    #         title="VECTOR RETRIEVER RESULTS",
    #     )

    #     print_results(
    #         query=query,
    #         results=bm25_results,
    #         title="BM25 RETRIEVER RESULTS",
    #     )


if __name__ == "__main__":
    main()