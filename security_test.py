import os
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from KH4NK1.agent.main import app, BASE_DIR

client = TestClient(app)

def test_legitimate_file_creation():
    path = "legit.txt"
    content = "legitimate content"

    response = client.post("/execute/task", json={
        "action": "create_file",
        "parameters": {
            "path": path,
            "content": content
        }
    })

    assert response.status_code == 200
    assert os.path.exists(path)
    with open(path, "r") as f:
        assert f.read() == content

    if os.path.exists(path):
        os.remove(path)

def test_path_traversal_blocked():
    path = "../evil_outside.txt"
    content = "should not be created"

    response = client.post("/execute/task", json={
        "action": "create_file",
        "parameters": {
            "path": path,
            "content": content
        }
    })

    assert response.status_code == 400
    assert "Access denied" in response.json()["detail"]
    assert not os.path.exists(path)

def test_absolute_path_outside_blocked():
    path = "/tmp/evil_absolute.txt"
    content = "should not be created"

    response = client.post("/execute/task", json={
        "action": "create_file",
        "parameters": {
            "path": path,
            "content": content
        }
    })

    assert response.status_code == 400
    assert "Access denied" in response.json()["detail"]
    assert not os.path.exists(path)

def test_nested_legitimate_file_creation():
    path = "subdir/nested_legit.txt"
    content = "nested content"

    response = client.post("/execute/task", json={
        "action": "create_file",
        "parameters": {
            "path": path,
            "content": content
        }
    })

    assert response.status_code == 200
    assert os.path.exists(path)

    if os.path.exists(path):
        os.remove(path)
    if os.path.exists("subdir"):
        os.rmdir("subdir")

def test_install_deps_validation():
    path = "../../etc/passwd"

    response = client.post("/execute/task", json={
        "action": "install_deps",
        "parameters": {
            "requirements_path": path
        }
    })

    assert response.status_code == 400
    assert "Access denied" in response.json()["detail"]

if __name__ == "__main__":
    pytest.main(["-s", __file__])
