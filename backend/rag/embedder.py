from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

class Embedder:
    def __init__(self):
        self.client = InferenceClient(token=os.getenv("hf_api_key"))
        # Use a model that supports embeddings via feature_extraction
        self.model = "sentence-transformers/all-MiniLM-L6-v2"

    def encode(self, texts):
        embeddings = []
        for text in texts:
            embedding = self.client.feature_extraction(text, model=self.model)
            embeddings.append(embedding)
        return embeddings
