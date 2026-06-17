#Step 1: Define the Data Models
#Raw Document Model and Chunk Document Model
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RawDocument:
    doc_id: str
    source_type: str
    path: str
    title: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    
@dataclass
class ChunkDocument:
    chunk_id: str
    doc_id: str
    source_type: str
    path: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    
