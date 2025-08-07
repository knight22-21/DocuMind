from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from backend.api.routes.upload import router as upload_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

app.include_router(upload_router, prefix="/api")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
