"""
This module defines the routes for managing books in the application.
"""

from flask import Blueprint, jsonify, request

books_bp = Blueprint("books", __name__)


@books_bp.route("", methods=["GET"])
def get_books():
    """Return list of books"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    category = request.args.get("category")
    # Retrieve from db

    return jsonify(
        {"books": [], "page": page, "per_page": per_page, "category": category}
    )


@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book_by_id(book_id: int):
    """Get a specific book based on its id"""
    # Query book by id
    return jsonify({"id": book_id})


@books_bp.route("", methods=["POST"])
def create_book():
    """Create a new book"""
    pass


@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id: int):
    """Get a specific book"""
    pass


@books_bp.route("/<int:book_id>", methods=["PUT"])
def update_book(book_id: int):
    """Update a book"""
    pass


@books_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id: int):
    """Delete a book"""
    pass


# Sub-resources
@books_bp.route("/<int:book_id>/reviews", methods=["GET"])
def get_book_reviews(book_id: int):
    """Get reviews for a book"""
    pass
