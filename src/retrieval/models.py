from dataclasses import dataclass, field
from typing import Any


@dataclass
class RetrievalResult:
    chunk_id: str
    doc_id: str
    content: str
    score: float
    rank: int
    retriever: str
    source_type: str
    path: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "doc_id": self.doc_id,
            "content": self.content,
            "score": self.score,
            "rank": self.rank,
            "retriever": self.retriever,
            "source_type": self.source_type,
            "path": self.path,
            "metadata": self.metadata,
        }