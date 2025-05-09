"""
This module contains simplified schemas for use in nested relationships
to avoid circular references.
"""

from app import ma
from app.models import Author, Book, Category, Publisher
from marshmallow import fields


class NestedAuthorSchema(ma.SQLAlchemySchema):
    """
    Simplified schema for Author when used in nested relationships.
    """

    class Meta:
        model = Author

    author_id = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()

    full_name = fields.Method("get_full_name")

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class NestedBookSchema(ma.SQLAlchemySchema):
    """
    Simplified schema for Book when used in nested relationships.
    """

    class Meta:
        model = Book

    book_id = ma.auto_field()
    title = ma.auto_field()
    isbn = ma.auto_field()


class NestedCategorySchema(ma.SQLAlchemySchema):
    """
    Simplified schema for Category when used in nested relationships.
    """

    class Meta:
        model = Category

    category_id = ma.auto_field()
    name = ma.auto_field()


class NestedPublisherSchema(ma.SQLAlchemySchema):
    """
    Simplified schema for Publisher when used in nested relationships.
    """

    class Meta:
        model = Publisher

    publisher_id = ma.auto_field()
    name = ma.auto_field()
    website = ma.auto_field()
