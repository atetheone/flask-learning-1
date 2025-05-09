import json
# import pytest
from app.constants import errors
# from datetime import date


def test_get_books(client, sample_data):
    """Test getting all books"""
    response = client.get("/api/books")
    assert response.status_code == 200

    retrieved_data = json.loads(response.data)
    assert "books" in retrieved_data
    books = retrieved_data["books"]

    assert len(books) == 2
    assert books[1]["title"] == "Test Book"
    assert books[0]["title"] == "Another Book"

    assert "pagination" in retrieved_data
    pagination = retrieved_data["pagination"]
    assert pagination["total_items"] == 2


def test_filter_books_by_title(client, sample_data):
    """Test filtering books by title."""
    response = client.get("/api/books?title=test")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data["books"]) == 1
    assert data["books"][0]["title"] == "Test Book"


def test_filter_books_by_author(client, sample_data):
    """Test filtering books by author name."""
    response = client.get("/api/books?author_name=John")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data["books"]) == 1
    assert data["books"][0]["title"] == "Test Book"


def test_filter_books_by_category(client, sample_data):
    """Test filtering books by category ID."""
    category = sample_data["categories"][1][1]  # Non-Fiction
    response = client.get(f"/api/books?category={category}")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data["books"]) == 1
    assert data["books"][0]["title"] == "Another Book"


def test_filter_books_by_publisher(client, sample_data):
    """Test filtering books by publisher ID."""
    publisher_id = sample_data["publishers"][0]  # First publisher
    response = client.get(f"/api/books?publisher_id={publisher_id}")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data["books"]) == 1
    assert data["books"][0]["title"] == "Test Book"


def test_filter_sort_books_by_price(client, sample_data):
    """Test filtering and sorting books by price."""
    response = client.get("/api/books?sort_by=price&sort_order=desc")
    assert response.status_code == 200

    data = response.get_json()
    assert len(data["books"]) == 2
    assert data["books"][0]["title"] == "Another Book"
    assert data["books"][1]["title"] == "Test Book"


def test_filter_books_by_author_name(client, sample_data):
    """Test filtering books by author name."""
    response = client.get("/api/books?author_name=John")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data["books"]) == 1
    assert data["books"][0]["title"] == "Test Book"


def test_sorting_books(client, sample_data):
    """Test sorting books by different fields."""
    # Sort by price ascending
    response = client.get("/api/books?sort_by=price&sort_order=asc")
    assert response.status_code == 200

    data = json.loads(response.data)
    prices = [float(book["price"]) for book in data["books"]]
    assert prices == sorted(prices)


def test_get_book_by_id(client, sample_data):
    """Test getting a single book by ID"""
    book_id = sample_data["books"][0]
    response = client.get(f"/api/books/{book_id}")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data["title"] == "Test Book"
    assert data["isbn"] == "1234567890123"


def test_get_book_by_id_not_found(client):
    """Test getting a book with an invalid ID"""
    response = client.get("/api/books/999999")
    assert response.status_code == 404
    assert response.json["error"] == errors.BOOK_NOT_FOUND


def test_create_book(client, sample_data):
    """Test creating a new book"""
    book_data = {
        "title": "New Test Book",
        "isbn": "1122334455667",
        "price": 14.99,
        "stock": 5,
        "description": "A new test book",
        "publisher_id": sample_data["publishers"][0],
        "author_id": sample_data["authors"][0],
        "category_ids": [sample_data["categories"][0][0]],
    }

    response = client.post("/api/books", json=book_data)

    assert response.status_code == 201

    data = json.loads(response.data)

    assert data["title"] == "New Test Book"
    assert float(data["price"]) == 14.99
    # assert data['author_id'] == sample_data['authors'][0]

    # Verify the book was actually added to the database
    book_id = data["book_id"]
    get_response = client.get(f"/api/books/{book_id}")
    assert get_response.status_code == 200


def test_create_book_invalid_content_type(client):
    """Test creating a book with invalid content type."""
    response = client.post("/api/books", data="invalid data")
    assert response.status_code == 415
    data = json.loads(response.data)
    assert "error" in data
    assert data["error"] == errors.INVALID_CONTENT_TYPE


def test_create_book_invalid_data(client):
    """Test creating a book with invalid data"""
    invalid_data = {
        "title": "",  # Invalid: empty title
        "isbn": "123",  # Invalid: too short ISBN
        "price": -5,  # Invalid: negative price
        "stock": -1,  # Invalid: negative stock
        "description": "",
        "publisher_id": 9999,  # Invalid: non-existent publisher
        "author_id": 9999,  # Invalid: non-existent author
        "category_ids": [9999],  # Invalid: non-existent category
    }
    response = client.post("/api/books", json=invalid_data)
    assert response.status_code == 404  # ++ 400 but 404 for now, TO BE FIXED


def test_create_book_missing_fields(client, sample_data):
    """Test creating a book with missing required fields."""
    incomplete_book = {
        "title": "Incomplete Book",
        # Missing ISBN
        "price": 12.99,
        "author_id": sample_data["authors"][0],
        # Missing publisher_id
    }

    response = client.post("/api/books", json=incomplete_book)

    assert response.status_code == 400
    data = json.loads(response.data)
    print(data)
    assert "error" in data
    assert data["error"] == errors.MISSING_REQUIRED_FIELD.format(field="isbn")


def test_create_book_invalid_author(client, sample_data):
    """Test creating a book with an invalid author."""
    invalid_author_book = {
        "title": "Invalid Author Book",
        "isbn": "978-3-16-148410-0",
        "price": 12.99,
        "author_id": 9999,  # Invalid author ID
        "publisher_id": sample_data["publishers"][0],
    }

    response = client.post("/api/books", json=invalid_author_book)

    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert data["error"] == errors.AUTHOR_NOT_FOUND


def test_create_book_invalid_publisher(client, sample_data):
    """Test creating a book with an invalid publisher."""
    invalid_publisher_book = {
        "title": "Invalid Publisher Book",
        "isbn": "978-3-16-148410-0",
        "price": 12.99,
        "author_id": sample_data["authors"][0],
        "publisher_id": 9999,  # Invalid publisher ID
    }
    response = client.post("/api/books", json=invalid_publisher_book)
    assert response.status_code == 404
    data = json.loads(response.data)

    assert "error" in data
    assert data["error"] == errors.PUBLISHER_NOT_FOUND


# Feature not implemented yet
def test_create_book_duplicate_isbn(client, sample_data):
    """Test creating a book with a duplicate ISBN."""
    book_id = sample_data["books"][1]

    # Use an existing ISBN from another book
    existing_isbn = client.get(f"/api/books/{book_id}").json["isbn"]
    duplicate_isbn_book = {
        "title": "Duplicate ISBN Book",
        "isbn": existing_isbn,
        "price": 12.99,
        "author_id": sample_data["authors"][0],
        "publisher_id": sample_data["publishers"][0],
    }

    response = client.post("/api/books", json=duplicate_isbn_book)

    assert response.status_code == 409
    data = json.loads(response.data)
    assert "error" in data
    assert data["error"] == errors.DUPLICATE_ISBN


def test_update_book(client, sample_data):
    """Test updating a book"""
    book_id = sample_data["books"][0]

    updated_data = {
        "title": "Updated Book Title",
        "price": 29.99,
        "isbn": "1234567890123",
        "publication_date": "2023-10-01",
        "stock": 15,
        "description": "Updated description",
        "publisher_id": sample_data["publishers"][0],
        "author_id": sample_data["authors"][0],
        "category_ids": [sample_data["categories"][0][0]],  # Valid category ID
    }
    response = client.put(f"/api/books/{book_id}", json=updated_data)

    assert response.status_code == 200

    data = json.loads(response.data)
    assert data["title"] == "Updated Book Title"
    assert float(data["price"]) == 29.99
    assert data["stock"] == 15
    assert data["description"] == "Updated description"


def test_update_book_invalid_date(client, sample_data):
    """Test updating a book with an invalid date.

    Args:
        client: The test client for making requests to the API.
        sample_data: Sample data for testing.
    """
    book_id = sample_data["books"][0]

    # Invalid date format
    update_data = {
        "publication_date": "invalid-date-format",
    }

    response = client.put(f"/api/books/{book_id}", json=update_data)

    assert response.status_code == 400

    data = json.loads(response.data)
    assert "error" in data
    assert data["error"] == errors.INVALID_DATE_FORMAT


def test_update_book_duplicate_isbn(client, sample_data):
    """Test updating a book with a duplicate ISBN."""
    book_id = sample_data["books"][0]
    second_book_id = sample_data["books"][1]

    # Use an existing ISBN from another book
    existing_isbn = client.get(f"/api/books/{second_book_id}").json["isbn"]
    print(existing_isbn)
    update_data = {
        "isbn": existing_isbn,
    }

    response = client.put(f"/api/books/{book_id}", json=update_data)

    assert response.status_code == 409  # ++ 409 but 400 for now, TO BE FIXED
    data = json.loads(response.data)
    assert data["error"] == errors.DUPLICATE_ISBN


def test_update_book_not_found(client):
    """Test updating a book that doesn't exist."""
    update_data = {"title": "This Book Does Not Exist"}

    response = client.put(
        "/api/books/9999", json=update_data
    )

    assert response.status_code == 404

    data = json.loads(response.data)

    assert "error" in data
    assert data["error"] == errors.BOOK_NOT_FOUND


def test_update_book_invalid_content_type(client, sample_data):
    """Test updating a book with invalid content type."""
    book_id = sample_data["books"][0]
    response = client.put(f"/api/books/{book_id}", data="invalid data")
    assert response.status_code == 415


def test_update_book_invalid_author(client, sample_data):
    """Test updating a book with an invalid author ID."""
    book_id = sample_data["books"][0]
    update_data = {"author_id": 9999}
    response = client.put(f"/api/books/{book_id}", json=update_data)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == errors.AUTHOR_NOT_FOUND


def test_update_book_invalid_publisher(client, sample_data):
    """Test updating a book with an invalid publisher ID."""
    book_id = sample_data["books"][0]
    update_data = {"publisher_id": 9999}
    response = client.put(f"/api/books/{book_id}", json=update_data)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == errors.PUBLISHER_NOT_FOUND


def test_update_book_invalid_category(client, sample_data):
    """Test updating a book with an invalid category ID."""
    book_id = sample_data["books"][0]
    update_data = {"category_ids": [9999]}
    response = client.put(f"/api/books/{book_id}", json=update_data)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == errors.CATEGORY_NOT_FOUND


def test_delete_book(client, sample_data):
    """Test deleting a book."""
    book_id = sample_data["books"][0]

    # Delete the book
    response = client.delete(f"/api/books/{book_id}")
    assert response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/api/books/{book_id}")
    assert get_response.status_code == 404

    # Check that we now have one book in total
    all_books = client.get("/api/books")
    data = json.loads(all_books.data)
    assert data["pagination"]["total_items"] == 1


def test_delete_nonexistent_book(client):
    """Test deleting a book that doesn't exist."""
    response = client.delete("/api/books/9999")
    assert response.status_code == 404
    data = json.loads(response.data)

    assert data["error"] == errors.BOOK_NOT_FOUND
