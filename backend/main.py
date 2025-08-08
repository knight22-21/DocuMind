from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from dotenv import load_dotenv
import os
from backend.api.routes.query import router as query_router

load_dotenv() 

from backend.api.routes.upload import router as upload_router

app = FastAPI()

from backend.api.routes.debug import router as debug_router
app.include_router(debug_router, prefix="/api")

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

app.include_router(upload_router, prefix="/api")
app.include_router(query_router, prefix="/api")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
