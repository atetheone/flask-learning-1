"""
Author Schema
This module defines the AuthorSchema class, which is used for serializing and
deserializing Author objects. It uses Marshmallow for schema definition and
validation.
"""

from app.models import Author
from app import ma
from marshmallow import fields
from app.schemas import NestedBookSchema


class AuthorSchema(ma.SQLAlchemySchema):
    """
    Schema for serializing and deserializing Author objects.
    """

    class Meta:
        """
        Meta class for AuthorSchema.
        Defines the model associated with this schema.
        """

        model = Author

    author_id = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    birth_date = ma.auto_field()
    biography = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

    full_name = fields.Method("get_full_name")

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    # Add the books field using the nested schema
    books = ma.Nested(NestedBookSchema, many=True)

    # Add url for nested resource
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("authors.get_author", values=dict(author_id="<author_id>")),
            "books": ma.URLFor(
                "authors.get_author_books", values=dict(author_id="<author_id>")
            ),
        }
    )
