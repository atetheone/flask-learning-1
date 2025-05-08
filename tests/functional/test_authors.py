from datetime import datetime
import pytest
import json
from app.constants import errors


def test_get_authors(client, sample_data):
    """Test retrieving all authors"""
    response = client.get('/api/authors')
    assert response.status_code == 200
    data = json.loads(response.data)
    authors = data['authors']
    assert len(authors) == 2
    assert authors[0]['first_name'] == 'John'
    assert authors[1]['first_name'] == 'Jane'
    assert data['pagination']['total_items'] == 2
    assert data['pagination']['total_pages'] == 1
    assert data['pagination']['current_page'] == 1


def test_get_authors_with_filters(client, sample_data):
    """Test retrieving authors with filters"""
    response = client.get('/api/authors?name=John')
    assert response.status_code == 200
    data = json.loads(response.data)
    authors = data['authors']
    assert len(authors) == 1
    assert authors[0]['first_name'] == 'John'
    assert data['pagination']['total_items'] == 1


def test_get_author_by_id(client, sample_data):
    """Test retrieving a single author by ID"""
    response = client.get('/api/authors/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['first_name'] == 'John'
    assert data['last_name'] == 'Doe'


def test_get_author_by_id_not_found(client):
    """Test retrieving a non-existent author"""
    response = client.get('/api/authors/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == errors.AUTHOR_NOT_FOUND


def test_get_author_books(client, sample_data):
    """Test retrieving all books by a specific author"""
    author_id = sample_data['authors'][0]
    response = client.get(f'/api/authors/{author_id}/books')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['title'] == 'Test Book'


def test_get_author_books_not_found(client):
    """Test retrieving books for a non-existent author"""
    response = client.get('/api/authors/999/books')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == errors.AUTHOR_NOT_FOUND


def test_create_author(client, sample_data):
    """Test creating a new author"""
    new_author = {
        'first_name': 'New',
        'last_name': 'Author',
        'biography': 'A new author biography',
        # 'birth_date': datetime(1990, 1, 1)
        # TO DO: python date to sqlachemy date
    }
    response = client.post('/api/authors', json=new_author)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['first_name'] == 'New'
    assert data['last_name'] == 'Author'


def test_create_author_missing_required_fields(client):
    """Test creating an author with missing required fields"""
    new_author = {
        'first_name': 'New'
    }
    response = client.post('/api/authors', json=new_author)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == errors.NAME_REQUIRED


def test_create_author_invalid_content_type(client):
    """Test creating an author with invalid content type"""
    response = client.post('/api/authors', data='Invalid data')
    assert response.status_code == 415
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == errors.INVALID_CONTENT_TYPE
