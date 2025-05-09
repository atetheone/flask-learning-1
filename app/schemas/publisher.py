"""
Publisher Schema
This module defines the PublisherSchema class, which is used for serializing
and deserializing Publisher objects.
"""

from app import ma
from app.models import Publisher


class PublisherSchema(ma.SQLAlchemySchema):
    """
    Schema for serializing and deserializing Publisher objects.
    """

    class Meta:
        """
        Meta class for PublisherSchema.
        """

        model = Publisher
        include_fk = True

    publisher_id = ma.auto_field()
    name = ma.auto_field()
    address = ma.auto_field()
    website = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor(
                "publishers.get_publisher",
                values=dict(publisher_id="<publisher_id>")
            ),
            "books": ma.URLFor(
                "publishers.get_publisher_books",
                values=dict(publisher_id="<publisher_id>")
            ),
        }
    )
