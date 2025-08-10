import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.api.routes.arxiv import router as arxiv_router
from backend.api.routes.debug import router as debug_router
from backend.api.routes.query import router as query_router
from backend.api.routes.upload import router as upload_router
from backend.api.routes.health import router as health_router

# Load environment variables
load_dotenv()

# Ensure upload directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

app = FastAPI()

# Mount static and uploads directories
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
uploads_path = Path(__file__).parent / "uploads"
app.mount("/uploads", StaticFiles(directory=uploads_path), name="uploads")

# Set up templates
templates = Jinja2Templates(directory="frontend/templates")

# Register API routers
app.include_router(debug_router, prefix="/api")
app.include_router(upload_router, prefix="/api")
app.include_router(query_router, prefix="/api")
app.include_router(arxiv_router, prefix="/api")
app.include_router(health_router)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
