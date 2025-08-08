from fastapi import APIRouter, UploadFile, File
from backend.services.pdf_reader import extract_text_from_pdf
from backend.core.config import UPLOAD_DIR
from backend.rag.chunker import chunk_text
from backend.rag.embedder import Embedder
from backend.rag.qdrant_client import init_collection, add_documents
from backend.services.llm_interface import summarize_text
import shutil

router = APIRouter()
embedder = Embedder()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    text = extract_text_from_pdf(str(file_path))

    # Chunk text
    chunks = chunk_text(text)

    # Generate embeddings
    embeddings = embedder.encode(chunks)

    # Init & upload to Qdrant
    init_collection(dim=len(embeddings[0]))
    add_documents(chunks, embeddings, metadata={"source": file.filename})

    summary = summarize_text(text)

    return {
        "filename": file.filename,
        "chunks_uploaded": len(chunks),
        "summary": summary,
        "preview": chunks[0][:300]
    }
