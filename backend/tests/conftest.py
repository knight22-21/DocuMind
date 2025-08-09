import io
import pytest
from fastapi.testclient import TestClient
from backend.main import app

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.fixture
def sample_pdf_file():
    pdf_content = b"%PDF-1.4\n%Test PDF content"
    return {"file": ("test.pdf", io.BytesIO(pdf_content), "application/pdf")}
