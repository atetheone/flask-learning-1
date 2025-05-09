"""
Category Schema
This module defines the CategorySchema class, which is used for serializing and
deserializing Category objects.
"""

from app import ma
from app.models import Category
from app.schemas import NestedBookSchema


class CategorySchema(ma.SQLAlchemySchema):
    """
    Schema for the Category model, defining fields and hyperlinks.
    """

    class Meta:
        """
        Meta class for CategorySchema to define model
        and additional configurations.
        """

        model = Category

    category_id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

    # Add the books field using the nested schema
    books = ma.Nested(NestedBookSchema, many=True)

    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor(
                "categories.get_category", values=dict(category_id="<category_id>")
            ),
            "books": ma.URLFor(
                "categories.get_category_books", values=dict(category_id="<category_id>")
            ),
        }
    )
