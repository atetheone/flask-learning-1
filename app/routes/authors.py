from flask import Blueprint, jsonify, request
from app import db
from app.models import Author, Book
from app.schemas import author_schema, authors_schema, books_schema

authors_bp = Blueprint("authors", __name__)


@authors_bp.route("", methods=["GET"])
def get_authors():
    """
    Get  all authors
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    authors_query = Author.query

    # Filters
    name_filter = request.args.get('name')
    if name_filter:
        authors_query = authors_query.filter(
            (Author.first_name.ilike(f'%{name_filter}%')) |
            (Author.last_name.ilike(f'%{name_filter}%'))
        )

    # Apply pagination
    pagination = authors_query.order_by(Author.last_name).paginate(
        page=page, per_page=per_page
    )

    return jsonify({
        "authors": authors_schema.dump(pagination.items),
        "pagination": {
            "total_items": pagination.total,
            "total_pages": pagination.pages,
            "current_page": page,
            "per_page": per_page
        }
    })


@authors_bp.route('', methods=['POST'])
def create_author():
    """Create a new author"""
    if not request.is_json():
        return jsonify({
            "error": "Invalid content type, expected JSON"
        }, 415)

    data = request.get_json()
    
    # Validate required fields
    if not data.get('first_name') or not data.get('last_name'):
        return jsonify({'error': 'First and last name are required'}), 400

    author = Author(
        first_name=data['first_name'],
        last_name=data['last_name'],
        birth_date=data.get('birth_date'),
        biography=data.get('biography')
    )

    db.session.add(author)
    db.session.commit()

    return jsonify(author_schema.dump(author)), 201


@authors_bp.route('/<int:author_id>', methods=['GET'])
def get_author(author_id):
    """Get a specific author by ID"""
    author = Author.query.get_or_404(author_id)
    return jsonify(author_schema.dump(author))


@authors_bp.route('/<int:author_id>/books', methods=['GET'])
def get_author_books(author_id):
    """Get all books by a specific author"""
    author = Author.query.get_or_404(author_id)
    books = author.books.all()
    return jsonify(books_schema.dump(books))
