import json
from app.constants import errors


def test_get_publishers(client, sample_data):
    """Test retrieving all publishers"""
    response = client.get("/api/publishers")
    assert response.status_code == 200
    data = json.loads(response.data)
    publishers = data["publishers"]
    assert len(publishers) == 2
    assert [
        publisher.get("name") in ["Test Publisher", "Another Press"]
        for publisher in publishers
    ]

    assert data["pagination"]["total_items"] == 2
    assert data["pagination"]["total_pages"] == 1
    assert data["pagination"]["current_page"] == 1


def test_get_publisher_by_id(client, sample_data):
    """Test retrieving a single publisher by ID"""
    publisher_id = sample_data["publishers"][0]
    response = client.get(f"/api/publishers/{publisher_id}")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data["name"] == "Test Publisher"


def test_get_publisher_by_id_not_found(client):
    """Test retrieving a non-existent publisher"""
    response = client.get("/api/publishers/999")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == errors.PUBLISHER_NOT_FOUND


def test_get_publisher_books(client, sample_data):
    """Test retrieving all books by a specific publisher"""
    publisher_id = sample_data["publishers"][0]
    response = client.get(
        f"/api/publishers/{publisher_id}/books?page=1&per_page=10"
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data["books"]) == 1
    assert data["books"][0]["title"] == "Test Book"


def test_get_publisher_books_not_found(client):
    """Test retrieving books for a non-existent publisher"""
    response = client.get("/api/publishers/999/books")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == errors.PUBLISHER_NOT_FOUND


def test_create_publisher(client):
    """Test creating a new publisher"""
    new_publisher = {
        "name": "New Publisher"
    }
    response = client.post("/api/publishers", json=new_publisher)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["name"] == new_publisher["name"]


def test_create_publisher_empty_name(client):
    """Test creating a publisher with empty name"""
    new_publisher = {
        "name": ""
    }
    response = client.post("/api/publishers", json=new_publisher)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["error"] == errors.EMPTY_FIELD.format(field="name")


def test_create_publisher_invalid_json(client):
    """Test creating a publisher with invalid JSON"""
    response = client.post("/api/publishers", data="Invalid JSON")
    assert response.status_code == 415
    data = json.loads(response.data)

    assert data["error"] == errors.INVALID_CONTENT_TYPE


def test_create_publisher_duplicate(client, sample_data):
    """Test creating a publisher with a duplicate name"""
    duplicate_publisher = {
        "name": "Test Publisher"
    }
    response = client.post("/api/publishers", json=duplicate_publisher)
    assert response.status_code == 409
    data = json.loads(response.data)
    assert data["error"] == errors.PUBLISHER_ALREADY_EXISTS
