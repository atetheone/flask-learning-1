# Bookstore Inventory API

A RESTful API for managing a bookstore's inventory system with Flask and SQLAlchemy. This project demonstrates database modeling, relationship management, and CRUD operations with a persistent data layer.

## Project Overview

This API provides endpoints to manage a bookstore inventory system with the following resources:
- Books
- Authors
- Categories
- Publishers

The system allows for complex queries, filtering, pagination, and managing relationships between entities.

## Features

- **Complete CRUD Operations** for all resources
- **Relational Data Model** with properly defined relationships:
  - One author can have many books
  - One publisher can have many books
  - Many books can belong to many categories
- **Advanced Filtering** by various attributes
- **Sorting** by different fields
- **Pagination** for all list endpoints
- **Data Validation** for all inputs
- **HATEOAS Links** for API navigation
- **Error Handling** with appropriate status codes

## Tech Stack

- **Flask**: Web framework
- **SQLAlchemy**: ORM for database interactions
- **SQLite**: Database (configurable for other databases)
- **Marshmallow**: Serialization/deserialization library
- **Flask-Marshmallow**: Flask integration for Marshmallow

## Project Structure

```
bookstore-api/
│
├── app/                           # Main application package
│   ├── __init__.py                # Application factory
│   │
│   ├── models/                    # Database models
│   │   ├── __init__.py            
│   │   ├── author.py              
│   │   ├── book.py                
│   │   ├── category.py            
│   │   └── publisher.py           
│   │
│   ├── schemas/                   # Serialization schemas
│   │   ├── __init__.py            
│   │   ├── author.py              
│   │   ├── book.py                
│   │   ├── category.py            
│   │   └── publisher.py           
│   │
│   ├── routes/                    # API routes
│   │   ├── __init__.py            
│   │   ├── authors.py             
│   │   ├── books.py               
│   │   ├── categories.py          
│   │   └── publishers.py          
│   │
│   └── utils/                     # Utility functions
│       ├── __init__.py
│       └── helpers.py
│
├── config.py                      # Configuration settings
├── requirements.txt               # Project dependencies
└── run.py                         # Application entry point
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd bookstore-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (optional):
   ```bash
   export FLASK_APP=run.py
   export FLASK_ENV=development
   ```

5. Initialize the database:
   ```bash
   flask shell
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

## Running the API

Start the development server:
```bash
flask run
```

The API will be available at `http://localhost:5000/`.

## API Endpoints

### Books

- `GET /api/books` - List all books (with pagination and filtering)
- `POST /api/books` - Create a new book
- `GET /api/books/<id>` - Get a specific book
- `PUT /api/books/<id>` - Update a book
- `DELETE /api/books/<id>` - Delete a book

### Authors

- `GET /api/authors` - List all authors
- `POST /api/authors` - Create a new author
- `GET /api/authors/<id>` - Get a specific author
- `PUT /api/authors/<id>` - Update an author
- `DELETE /api/authors/<id>` - Delete an author
- `GET /api/authors/<id>/books` - Get all books by an author

### Categories

- `GET /api/categories` - List all categories
- `POST /api/categories` - Create a new category
- `GET /api/categories/<id>` - Get a specific category
- `PUT /api/categories/<id>` - Update a category
- `DELETE /api/categories/<id>` - Delete a category
- `GET /api/categories/<id>/books` - Get all books in a category

### Publishers

- `GET /api/publishers` - List all publishers
- `POST /api/publishers` - Create a new publisher
- `GET /api/publishers/<id>` - Get a specific publisher
- `PUT /api/publishers/<id>` - Update a publisher
- `DELETE /api/publishers/<id>` - Delete a publisher
- `GET /api/publishers/<id>/books` - Get all books from a publisher

## Query Parameters

Many endpoints support the following query parameters:

- `page` - Page number for pagination (default: 1)
- `per_page` - Items per page (default: 10, max: 100)
- `sort_by` - Field to sort by
- `sort_order` - Sort direction (`asc` or `desc`)

Book-specific filters:
- `title` - Filter by book title (partial match)
- `author` - Filter by author name
- `category_id` - Filter by category ID
- `publisher_id` - Filter by publisher ID

## Examples

### Creating a New Author

**Request:**
```http
POST /api/authors
Content-Type: application/json

{
  "first_name": "Jane",
  "last_name": "Austen",
  "birth_date": "1775-12-16",
  "biography": "Jane Austen was an English novelist known primarily for her six major novels."
}
```

**Response:**
```json
{
  "id": 1,
  "first_name": "Jane",
  "last_name": "Austen",
  "full_name": "Jane Austen",
  "birth_date": "1775-12-16",
  "biography": "Jane Austen was an English novelist known primarily for her six major novels.",
  "created_at": "2023-05-01T14:30:45",
  "updated_at": "2023-05-01T14:30:45",
  "_links": {
    "self": "/api/authors/1",
    "books": "/api/authors/1/books"
  }
}
```

### Getting Books with Filtering

**Request:**
```http
GET /api/books?title=pride&sort_by=publication_date&sort_order=desc&page=1&per_page=10
```

**Response:**
```json
{
  "books": [
    {
      "id": 3,
      "title": "Pride and Prejudice",
      "isbn": "9780141439518",
      "publication_date": "1813-01-28",
      "price": 9.99,
      "stock": 15,
      "author_id": 1,
      "publisher_id": 2,
      "_links": {
        "self": "/api/books/3",
        "author": "/api/authors/1",
        "publisher": "/api/publishers/2"
      }
    }
  ],
  "pagination": {
    "total_items": 1,
    "total_pages": 1,
    "current_page": 1,
    "per_page": 10
  }
}
```

## Learning Outcomes

This project demonstrates:

1. **Database Design** - Proper modeling of relational data
2. **RESTful API Design** - Following best practices for resource naming and HTTP methods
3. **Query Optimization** - Efficient database queries with filtering and pagination
4. **Data Validation** - Input validation for all API operations
5. **API Documentation** - Clear documentation of endpoints and their behavior

## Next Steps

Potential enhancements for this project:
- Add authentication and authorization
- Implement more advanced search capabilities
- Add caching for improved performance
- Create a front-end interface
- Add API versioning
- Implement rate limiting

## License

This project is licensed under the MIT License - see the LICENSE file for details.