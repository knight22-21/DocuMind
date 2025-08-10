import io
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from reportlab.pdfgen import canvas


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture
def sample_pdf_file():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, "Hello, this is a test PDF.")
    c.save()
    buffer.seek(0)
    return {"file": ("test.pdf", buffer, "application/pdf")}
