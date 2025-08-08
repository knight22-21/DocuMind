from qdrant_client import QdrantClient
from qdrant_client.http.models import SearchRequest, Filter, Payload, PayloadSelector
from backend.rag.embedder import Embedder
import os

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
embedder = Embedder()

def retrieve_relevant_chunks(query: str, top_k: int = 5) -> list[dict]:
    query_vector = embedder.encode([query])[0]

    hits = client.search(
        collection_name="research_papers",
        query_vector=query_vector,
        limit=top_k,
        with_payload=True
    )

    return [
        {
            "text": hit.payload["text"],
            "source": hit.payload["source"],
            "score": hit.score
        }
        for hit in hits
    ]
