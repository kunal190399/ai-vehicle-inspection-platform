import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from app.api import app
client=TestClient(app)
def test_health():
    assert client.get("/health").json()["status"]=="ok"
def test_reject_non_image():
    r=client.post("/inspections",files={"image":("x.txt",b"hello","text/plain")})
    assert r.status_code==400
