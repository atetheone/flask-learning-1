from app.constants import errors
from app.models.book import Book
from app.schemas import category_schema, categories_schema, books_schema
from app.models import Category
from app import db
from flask import Blueprint, jsonify, request

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("", methods=["GET"])
def get_categories():
    """
    Get all categories
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    categories_query = db.session.query(Category)

    # Apply pagination
    pagination = categories_query.order_by(Category.name).paginate(
        page=page, per_page=per_page
    )

    return jsonify(
        {
            "categories": categories_schema.dump(pagination.items),
            "pagination": {
                "total_items": pagination.total,
                "total_pages": pagination.pages,
                "current_page": page,
                "per_page": per_page,
            },
        }
    )


@categories_bp.route("/<int:category_id>", methods=["GET"])
def get_category(category_id: int):
    """Get a single category by ID"""
    category = db.session.query(Category).get(category_id)
    if not category:
        return jsonify({"error": errors.CATEGORY_NOT_FOUND}), 404

    return jsonify(category_schema.dump(category))


@categories_bp.route("/<int:category_id>/books", methods=["GET"])
def get_category_books(category_id: int):
    """Get all books in a specific category"""
    category = db.session.query(Category).get(category_id)
    if not category:
        return jsonify({"error": errors.CATEGORY_NOT_FOUND}), 404

    # Paginate books in the category
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    books_query = db.session.query(Book).filter(
        Category.category_id == category_id
    )

    # Apply pagination
    pagination = books_query.paginate(page=page, per_page=per_page)

    return jsonify(
        {
            "category": {"id": category.category_id, "name": category.name},
            "books": books_schema.dump(pagination.items),
            "pagination": {
                "total_items": pagination.total,
                "total_pages": pagination.pages,
                "current_page": page,
                "per_page": per_page,
            },
        }
    )


@categories_bp.route("", methods=["POST"])
def create_category():
    """Create a new category"""
    data = request.get_json()

    # Validate required fields
    if not data.get("name"):
        return (
            jsonify({
                "error": errors.MISSING_REQUIRED_FIELD.format(field="name")
            }),
            400,
        )

    # Check if category already exists
    existing_category = (
        db.session.query(Category)
        .filter_by(name=data["name"])
        .first()
    )
    if existing_category:
        return jsonify({"error": errors.DUPLICATE_CATEGORY}), 400

    category = Category(
        name=data["name"],
        description=data.get("description"),
    )

    db.session.add(category)
    db.session.commit()

    return jsonify(category_schema.dump(category)), 201


@categories_bp.route("/<int:category_id>", methods=["PUT"])
def update_category(category_id: int):
    """Update an existing category"""
    data = request.get_json()
    category = db.session.get(Category, category_id)
    if not category:
        return jsonify({"error": errors.CATEGORY_NOT_FOUND}), 404

    # Validate required fields
    if "name" in data and not data["name"]:
        return jsonify({"error": errors.EMPTY_FIELD.format(field="name")}), 400

    # Check if category already exists
    existing_category = (
        db.session.query(Category)
        .filter_by(name=data["name"])
        .first()
    )
    if existing_category and existing_category.category_id != category_id:
        return jsonify({"error": errors.DUPLICATE_CATEGORY}), 400

    category.name = data["name"]
    category.description = data.get("description")

    db.session.commit()

    return jsonify(category_schema.dump(category))


@categories_bp.route("/<int:category_id>", methods=["DELETE"])
def delete_category(category_id: int):
    """Delete a category"""
    category = db.session.get(Category, category_id)
    if not category:
        return jsonify({"error": errors.CATEGORY_NOT_FOUND}), 404

    # Check if the category has books
    if category.books:
        return jsonify({"error": errors.CATEGORY_HAS_BOOKS}), 400

    db.session.delete(category)
    db.session.commit()

    return "", 204
