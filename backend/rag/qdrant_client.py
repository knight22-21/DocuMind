import os
from uuid import uuid4
from typing import List
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct

# Load .env variables
load_dotenv()

# Qdrant config
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = "research_papers"

# Initialize client 
client = QdrantClient(
    url=QDRANT_URL,           
    api_key=QDRANT_API_KEY    
)

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
