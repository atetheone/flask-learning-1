from app.schemas import publisher_schema, publishers_schema, books_schema
from app.models import Publisher, Book
from flask import Blueprint, request, jsonify
from app import db
from app.constants import errors

publishers_bp = Blueprint("publishers", __name__)


@publishers_bp.route("", methods=["GET"])
def get_publishers():
    """
    Get all publishers
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    publishers_query = db.session.query(Publisher)

    # Apply pagination
    pagination = publishers_query.order_by(Publisher.name).paginate(
        page=page, per_page=per_page
    )

    return jsonify(
        {
            "publishers": publishers_schema.dump(pagination.items),
            "pagination": {
                "total_items": pagination.total,
                "total_pages": pagination.pages,
                "current_page": page,
                "per_page": per_page,
            },
        }
    )


@publishers_bp.route("/<int:publisher_id>", methods=["GET"])
def get_publisher(publisher_id: int):
    """Get a single publisher by ID"""
    publisher = db.session.get(Publisher, publisher_id)
    if not publisher:
        return jsonify({"error": errors.PUBLISHER_NOT_FOUND}), 404

    return jsonify(publisher_schema.dump(publisher))


@publishers_bp.route("/<int:publisher_id>/books", methods=["GET"])
def get_publisher_books(publisher_id: int):
    """Get all books by a specific publisher"""
    publisher = db.session.get(Publisher, publisher_id)
    if not publisher:
        return jsonify({"error": errors.PUBLISHER_NOT_FOUND}), 404

    # Paginate books by the publisher
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    books_query = db.session.query(Book).filter(Book.publisher_id == publisher_id)

    # Apply pagination
    pagination = books_query.order_by(Book.title).paginate(page=page, per_page=per_page)

    return jsonify(
        {
            "books": books_schema.dump(pagination.items),
            "pagination": {
                "total_items": pagination.total,
                "total_pages": pagination.pages,
                "current_page": page,
                "per_page": per_page,
            },
        }
    )


@publishers_bp.route("", methods=["POST"])
def create_publisher():
    """Create a new publisher"""
    if not request.is_json:
        return jsonify({"error": errors.INVALID_CONTENT_TYPE}), 415

    data = request.get_json()

    if 'name' in data and not data['name']:
        return jsonify({"error": errors.EMPTY_FIELD.format(field="name")}), 400

    try:
        new_publisher = Publisher(**data)
        db.session.add(new_publisher)
        db.session.commit()
    except Exception as e:
        print(f"Error creating publisher: {e}")
        db.session.rollback()
        return jsonify({"error": errors.PUBLISHER_ALREADY_EXISTS}), 409

    return jsonify(publisher_schema.dump(new_publisher)), 201
