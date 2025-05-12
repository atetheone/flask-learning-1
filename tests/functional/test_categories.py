# import pytest
import json
from app.constants import errors


def test_get_categories(client, sample_data):
    """Test retrieving all categories"""
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = json.loads(response.data)
    categories = data["categories"]
    assert len(categories) == 3
    assert [
        category.get("name") in ["Fiction", "Non-Fiction", "Science Fiction"]
        for category in categories
    ]

    assert data["pagination"]["total_items"] == 3
    assert data["pagination"]["total_pages"] == 1
    assert data["pagination"]["current_page"] == 1


def test_get_category_by_id(client, sample_data):
    """Test retrieving a single category by ID"""
    category_id = sample_data["categories"][0][0]
    response = client.get(f"/api/categories/{category_id}")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data["name"] == "Fiction"


def test_get_category_by_id_not_found(client):
    """Test retrieving a non-existent category"""
    response = client.get("/api/categories/999")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == errors.CATEGORY_NOT_FOUND


def test_get_category_books(client, sample_data):
    """Test retrieving all books in a specific category"""
    category_id = sample_data["categories"][0][0]
    response = client.get(
        f"/api/categories/{category_id}/books?page=1&per_page=10"
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data["books"]) == 1
    assert data["books"][0]["title"] == "Test Book"


def test_get_category_books_not_found(client):
    """Test retrieving books for a non-existent category"""
    response = client.get("/api/categories/999/books")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == errors.CATEGORY_NOT_FOUND


def test_create_category(client, sample_data):
    """Test creating a new category"""
    data = {"name": "New Category"}
    response = client.post("/api/categories", json=data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["name"] == "New Category"

    # Verify the category was created
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = json.loads(response.data)
    categories = data["categories"]
    assert len(categories) == 4


def test_create_category_missing_name(client):
    """Test creating a category with missing name"""
    data = {"description": "A new category without a name"}
    response = client.post("/api/categories", json=data)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["error"] == errors.MISSING_REQUIRED_FIELD.format(field="name")


def test_create_category_duplicate(client, sample_data):
    """Test creating a duplicate category"""
    data = {"name": "Fiction"}
    response = client.post("/api/categories", json=data)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["error"] == errors.DUPLICATE_CATEGORY


def test_update_category(client, sample_data):
    """Test updating an existing category"""
    category_id = sample_data["categories"][0][0]
    data = {"name": "Updated Category", "description": "An updated desc"}
    response = client.put(f"/api/categories/{category_id}", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["name"] == "Updated Category"

    # Verify the category was updated
    response = client.get(f"/api/categories/{category_id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["name"] == "Updated Category"


def test_update_category_not_found(client):
    """Test updating a non-existent category"""
    data = {"name": "Updated Category"}
    response = client.put("/api/categories/999", json=data)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == errors.CATEGORY_NOT_FOUND


def test_update_category_empty_name(client, sample_data):
    """Test updating a category with an empty name"""
    category_id = sample_data["categories"][0][0]
    data = {"name": ""}
    response = client.put(f"/api/categories/{category_id}", json=data)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["error"] == errors.EMPTY_FIELD.format(field="name")


def test_update_category_duplicate(client, sample_data):
    """Test updating a category to a name that already exists"""
    category_id = sample_data["categories"][0][0]

    data = {"name": "Non-Fiction"}
    response = client.put(f"/api/categories/{category_id}", json=data)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["error"] == errors.DUPLICATE_CATEGORY


def test_delete_category(client, sample_data):
    """Test deleting a category"""
    category_id = sample_data["categories"][2][0]
    response = client.delete(f"/api/categories/{category_id}")
    assert response.status_code == 204

    # Verify the category was deleted
    response = client.get(f"/api/categories/{category_id}")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == errors.CATEGORY_NOT_FOUND


def test_delete_category_not_found(client):
    """Test deleting a non-existent category"""
    response = client.delete("/api/categories/999")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == errors.CATEGORY_NOT_FOUND


def test_delete_category_with_books(client, sample_data):
    """Test deleting a category with existing books"""
    category_id = sample_data["categories"][0][0]
    response = client.delete(f"/api/categories/{category_id}")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["error"] == errors.CATEGORY_HAS_BOOKS
