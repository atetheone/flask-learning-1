# import pytest
import json
from app.constants import errors


def test_get_authors(client, sample_data):
    """Test retrieving all authors"""
    response = client.get('/api/authors')
    assert response.status_code == 200
    data = json.loads(response.data)
    authors = data['authors']
    print(authors)
    assert len(authors) == 3
    assert [
        author.get('first_name') in ['John', 'Jane', 'Bookless']
        for author in authors
    ]

    assert data['pagination']['total_items'] == 3
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


def test_update_author(client, sample_data):
    """Test updating an existing author"""
    author_id = sample_data['authors'][0]
    updated_author = {
        'first_name': 'Updated',
        'last_name': 'Author',
        'biography': 'An updated author biography',
        'birth_date': '1992-01-01'
    }
    response = client.put(f'/api/authors/{author_id}', json=updated_author)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['first_name'] == 'Updated'
    assert data['last_name'] == 'Author'


def test_update_author_not_found(client):
    """Test updating a non-existent author"""
    updated_author = {
        'first_name': 'Updated',
        'last_name': 'Author'
    }
    response = client.put('/api/authors/999', json=updated_author)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == errors.AUTHOR_NOT_FOUND


def test_update_author_empty_first_name(client, sample_data):
    """Test updating an author with an empty first name"""
    author_id = sample_data['authors'][0]
    updated_author = {
        'first_name': '',
        'last_name': 'Author'
    }
    response = client.put(f'/api/authors/{author_id}', json=updated_author)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == errors.EMPTY_FIELD.format(field='first_name')


def test_update_author_empty_last_name(client, sample_data):
    """Test updating an author with an empty last name"""
    author_id = sample_data['authors'][0]
    updated_author = {
        'first_name': 'Updated',
        'last_name': ''
    }
    response = client.put(f'/api/authors/{author_id}', json=updated_author)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == errors.EMPTY_FIELD.format(field='last_name')
    

def test_update_author_invalid_date_format(client, sample_data):
    """Test updating an author with an invalid date format"""
    author_id = sample_data['authors'][0]
    updated_author = {
        'first_name': 'Updated',
        'last_name': 'Author',
        'birth_date': 'InvalidDateFormat'
    }
    response = client.put(f'/api/authors/{author_id}', json=updated_author)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == errors.INVALID_DATE_FORMAT


def test_delete_author(client, sample_data):
    """Test deleting an author"""
    author_id = sample_data['authors'][2]
    response = client.delete(f'/api/authors/{author_id}')
    assert response.status_code == 204
    # Check if the author is actually deleted
    response = client.get(f'/api/authors/{author_id}')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == errors.AUTHOR_NOT_FOUND
    

def test_delete_author_not_found(client):
    """Test deleting a non-existent author"""
    response = client.delete('/api/authors/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == errors.AUTHOR_NOT_FOUND
    
    
def test_delete_author_with_books(client, sample_data):
    """Test deleting an author with existing books"""
    author_id = sample_data['authors'][0]
    # Create a book for the author
    new_book = {
        'title': 'New Book',
        'isbn': '1234567890123',
        'publication_date': '2023-01-01',
        'author_id': author_id
    }
    client.post('/api/books', json=new_book)
    
    response = client.delete(f'/api/authors/{author_id}')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == errors.AUTHOR_HAS_BOOKS