from flask import Blueprint, jsonify, request
from app import db
from app.constants import errors
from app.models import Author
from app.schemas import author_schema, authors_schema, books_schema
from app.utils import parse_date

authors_bp = Blueprint("authors", __name__)


@authors_bp.route("", methods=["GET"])
def get_authors():
    """
    Get  all authors
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    authors_query = Author.query

    # Filters
    name_filter = request.args.get("name")
    if name_filter:
        authors_query = authors_query.filter(
            (Author.first_name.ilike(f"%{name_filter}%"))
            | (Author.last_name.ilike(f"%{name_filter}%"))
        )

    # Apply pagination
    pagination = authors_query.order_by(Author.last_name).paginate(
        page=page, per_page=per_page
    )

    return jsonify(
        {
            "authors": authors_schema.dump(pagination.items),
            "pagination": {
                "total_items": pagination.total,
                "total_pages": pagination.pages,
                "current_page": page,
                "per_page": per_page,
            },
        }
    )


@authors_bp.route("", methods=["POST"])
def create_author():
    """Create a new author"""
    if not request.is_json:
        return jsonify({"error": errors.INVALID_CONTENT_TYPE}), 415

    data = request.get_json()

    # Validate required fields
    if not data.get("first_name") or not data.get("last_name"):
        return jsonify({"error": "First and last name are required"}), 400

    author = Author(
        first_name=data["first_name"],
        last_name=data["last_name"],
        birth_date=data.get("birth_date"),
        biography=data.get("biography"),
    )

    db.session.add(author)
    db.session.commit()

    return jsonify(author_schema.dump(author)), 201


@authors_bp.route("/<int:author_id>", methods=["GET"])
def get_author(author_id):
    """Get a specific author by ID"""
    author = db.session.get(Author, author_id)
    if not author:
        return jsonify({"error": "Author not found"}), 404
    # author = Author.query.get_or_404(author_id)

    return jsonify(author_schema.dump(author))


@authors_bp.route("/<int:author_id>/books", methods=["GET"])
def get_author_books(author_id):
    """Get all books by a specific author"""
    author = db.session.get(Author, author_id)
    if not author:
        return jsonify({"error": "Author not found"}), 404
    # author = Author.query.get_or_404(author_id)
    books = author.books.all()
    return jsonify(books_schema.dump(books))


@authors_bp.route("/<int:author_id>", methods=["PUT"])
def update_author(author_id: int):
    """Update an existing author"""

    author = db.session.get(Author, author_id)
    if not author:
        return jsonify({"error": errors.AUTHOR_NOT_FOUND}), 404

    data = request.get_json()

    if "first_name" in data:
        if not data["first_name"]:
            return (
                jsonify({"error": errors.EMPTY_FIELD.format(field="first_name")}),
                400,
            )
        author.first_name = data["first_name"]

    if "last_name" in data:
        if not data["last_name"]:
            return jsonify({"error": errors.EMPTY_FIELD.format(field="last_name")}), 400
        author.last_name = data["last_name"]

    if "birth_date" in data:
        try:
            author.birth_date = parse_date(data["birth_date"])
        except ValueError:
            return jsonify({"error": errors.INVALID_DATE_FORMAT}), 400

    if "biography" in data:
        author.biography = data.get("biography")

    db.session.commit()

    return jsonify(author_schema.dump(author))


@authors_bp.route("/<int:author_id>", methods=["DELETE"])
def delete_author(author_id: int):
    """Delete an author"""
    author = db.session.get(Author, author_id)
    if not author:
        return jsonify({"error": errors.AUTHOR_NOT_FOUND}), 404

    # Check if the author has books
    if author.books.count() > 0:
        return jsonify({"error": errors.AUTHOR_HAS_BOOKS}), 400

    db.session.delete(author)
    db.session.commit()

    return "", 204
