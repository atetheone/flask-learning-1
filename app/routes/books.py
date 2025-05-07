"""
This module defines the routes for managing books in the application.
"""

from flask import Blueprint, jsonify, request
from app import db
from app.models import Book, Author, Category, Publisher
from app.schemas import book_details_schema, books_schema, book_schema

books_bp = Blueprint("books", __name__)


@books_bp.route("", methods=["GET"])
def get_books():
    """Return all books with optional filters and pagination"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    category = request.args.get("category")

    # Retrieve from db
    books_query = Book.query

    # Apply filters
    title = request.args.get('title')
    if title:
        books_query = books_query.filter(
            Book.title.ilike(f'%{title}%')
        )

    # Filter by author name
    author_name = request.args.get('author_name')
    if author_name:
        books_query = books_query.join(Book.author).filter(
            (Author.first_name.ilike(f'%{author_name}%')) |
            (Author.last_name.ilike(f'%{author_name}%'))
        )

    # Filter by category
    category = request.args.get('category')
    if category:
        books_query = books_query.join(Book.categories).filter(
            Category.name.ilike(f'%{category}%')
        )

    # Filter by publisher
    publisher_id = request.args.get('publisher_id')
    if publisher_id:
        books_query = books_query.filter(
            Book.publisher_id == publisher_id
        )

    # Apply sorting
    sort_by = request.args.get('sort_by', 'title')
    sort_order = request.args.get('sort_order', 'asc')

    if sort_by == 'title':
        sort_column = Book.title
    elif sort_by == 'price':
        sort_column = Book.price
    elif sort_by == 'publication_date':
        sort_column = Book.publication_date
    else:
        sort_column = Book.title

    if sort_order == 'desc':
        books_query = books_query.order_by(sort_column.desc())
    else:
        books_query = books_query.order_by(sort_column.asc())

    # Apply pagination
    pagination = books_query.paginate(page=page, per_page=per_page)

    return jsonify(
        {
            "books": books_schema.dump(pagination.items),
            "pagination": {
                "total_items": pagination.total,
                "total_pages": pagination.pages,
                "current_page": page,
                "per_page": per_page,
            }
        }
    )


@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id: int):
    """Get a specific book"""
    book = Book.query.get_or_404(book_id)
    return jsonify(book_schema.dump(book))


@books_bp.route("", methods=["POST"])
def create_book():
    """Create a new book"""
    if not request.is_json:
        return jsonify({"error": "Invalid content type"}), 415
    data = request.get_json()

    # Validate input
    required_fields = ['title', 'isbn', 'price', 'author_id', 'publisher_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    return jsonify({"message": "Book created successfully"}), 201

    # Verify author and publisher exist
    author = Author.query.get(data['author_id'])
    if not author:
        return jsonify({'error': f'Author with id {data["author_id"]} not found'}), 404

    publisher = Publisher.query.get(data['publisher_id'])
    if not publisher:
        return jsonify({'error': f'Publisher with id {data["publisher_id"]} not found'}), 404

    # Create new book
    book = Book(
        title=data['title'],
        isbn=data['isbn'],
        price=data['price'],
        author_id=data['author_id'],
        publisher_id=data['publisher_id'],
        stock=data.get('stock', 0),
        description=data.get('description')
    )

    if 'category_ids' in data and isintance(data['category_ids'], list):
        for category_id in data['category_ids']:
            category = Category.query.get(category_id)
            if category:
                book.categories.append(category)

    db.session.add(book)
    db.session.commit()

    return jsonify(book_details_schema.dump(book)), 201


@books_bp.route("/<int:book_id>", methods=["PUT"])
def update_book(book_id: int):
    """Update a book"""
    book = Book.query.get_or_404(book_id)

    if not request.is_json:
        return jsonify({'error': 'Invalid content type'}), 415

    data = request.get_json()

    # Update fields
    if 'title' in data:
        book.title = data['title']
    if 'isbn' in data:
        book.isbn = data['isbn']
    if 'publication_date' in data:
        book.publication_date = data['publication_date']
    if 'price' in data:
        book.price = data['price']
    if 'stock' in data:
        book.stock = data['stock']
    if 'description' in data:
        book.description = data['description']

    if 'author_id' in data:
        author = Author.query.get(data['author_id'])
        if not author:
            return jsonify({'error': f'Author with ID {data["author_id"]} not found'}), 404
        book.author_id = data['author_id']

    if 'publisher_id' in data:
        publisher = Publisher.query.get(data['publisher_id'])
        if not publisher:
            return jsonify({'error': f'Publisher with ID {data["publisher_id"]} not found'}), 404
        book.publisher_id = data['publisher_id']

    if 'category_ids' in data:
        # Clear existing categories
        book.categories = []
        for category_id in data['category_ids']:
            category = Category.query.get(category_id)
            if not category:
                return jsonify({'error': f'Category with ID {category_id} not found'}), 404
            book.categories.append(category)

    db.session.commit()
    return jsonify(book_details_schema.dump(book))


@books_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id: int):
    """Delete a book"""
    book = Book.query.get_or_404(book_id)

    db.session.delete(book)
    db.session.commit()

    return '', 204


# Sub-resources
@books_bp.route("/<int:book_id>/reviews", methods=["GET"])
def get_book_reviews(book_id: int):
    """Get reviews for a book"""
    pass
