from fastapi import APIRouter, UploadFile, File
from backend.services.pdf_reader import extract_text_from_pdf
from backend.core.config import UPLOAD_DIR
import shutil

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(str(file_path))
    return {"filename": file.filename, "text_preview": text[:500]}
