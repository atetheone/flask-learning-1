"""
Book schema for serialization and deserialization using Marshmallow.
"""

from app import ma
from app.models import Book
from app.schemas import NestedAuthorSchema, NestedCategorySchema, NestedPublisherSchema


class BookSchema(ma.SQLAlchemySchema):
    """
    Schema for serializing and deserializing Book objects.
    """

    class Meta:
        """
        Meta class for defining schema metadata and configurations.
        """

        model = Book

    book_id = ma.auto_field()
    title = ma.auto_field()
    isbn = ma.auto_field()
    publication_date = ma.auto_field()
    price = ma.auto_field()
    stock = ma.auto_field()
    description = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()
    author_id = ma.auto_field()
    publisher_id = ma.auto_field()

    # Only include author and publisher IDs in the basic schema
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("books.get_book", values=dict(book_id="<book_id>")),
            "author": ma.URLFor(
                "authors.get_author", values=dict(author_id="<author_id>")
            ),
            "publisher": ma.URLFor(
                "publishers.get_publisher", values=dict(publisher_id="<publisher_id>")
            ),
            # publishers routes are not implemented yet
        }
    )


# More detailed schema that includes nested objects
class BookDetailsSchema(BookSchema):
    """
    Schema for detailed serialization and deserialization of Book objects,
    including nested author, publisher, and categories.
    """

    author = ma.Nested(NestedAuthorSchema)
    publisher = ma.Nested(NestedPublisherSchema)
    categories = ma.Nested(NestedCategorySchema, many=True)
