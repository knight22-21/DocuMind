from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct, CollectionStatus
from uuid import uuid4
from typing import List

COLLECTION_NAME = "research_papers"

client = QdrantClient(host="localhost", port=6333)

def init_collection(dim: int):
    existing = client.get_collections()
    if COLLECTION_NAME not in [c.name for c in existing.collections]:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
        )

def add_documents(texts: List[str], embeddings: List[List[float]], metadata: dict):
    points = [
        PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload={
                "text": text,
                "source": metadata["source"]
            }
        )
        for text, embedding in zip(texts, embeddings)
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=points)
