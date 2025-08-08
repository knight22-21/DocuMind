from fastapi import APIRouter
from dotenv import load_dotenv
import os

router = APIRouter()
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

@router.get("/debug/qdrant/points")
def debug_qdrant(limit: int = 5):
    response = client.scroll(
        collection_name="research_papers",
        limit=limit,
        with_payload=True,
        with_vectors=False
    )
    return {
        "points": [point.dict() for point in response[0]]
    }
