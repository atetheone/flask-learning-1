"""
Book schema for serialization and deserialization using Marshmallow.
"""

from app import ma
from app.models import Book
from app.schemas.author import AuthorSchema
from app.schemas.category import CategorySchema
from app.schemas.publisher import PublisherSchema


class BookSchema(ma.SQLAlchemySchema):
    """
    Schema for serializing and deserializing Book objects.
    """
    class Meta:
        """
        Meta class for defining schema metadata and configurations.
        """

        model = Book

        def get_model_name(self):
            """
            Returns the name of the model associated with this schema.
            """
            return self.model.__name__

        def get_fields(self):
            """
            Returns a list of fields defined in the schema.
            """
            return [field for field in dir(self) if not field.startswith("_")]

    book_id = ma.auto_field()
    title = ma.auto_field()
    isbn = ma.auto_field()
    publication_date = ma.auto_field()
    price = ma.auto_field()
    stock = ma.auto_field()
    description = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

    # Only include author and publisher IDs in the basic schema
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor(
                "books.get_book",
                values=dict(book_id="<book_id>")
            ),
            "author": ma.URLFor(
                "authors.get_author", values=dict(author_id="<author_id>")
            ),
            # "publisher": ma.URLFor(
            #     "publishers.get_publisher",
            #     values=dict(publisher_id="<publisher_id>")
            # ),
            # publishers routes are not implemented yet
        }
    )


# More detailed schema that includes nested objects
class BookDetailsSchema(BookSchema):
    """
    Schema for detailed serialization and deserialization of Book objects,
    including nested author, publisher, and categories.
    """
    author = ma.Nested(AuthorSchema, exclude=("books", "biography"))
    publisher = ma.Nested(
        PublisherSchema, exclude=("books", "created_at", "updated_at")
    )
    categories = ma.Nested(
        CategorySchema,
        many=True,
        exclude=("books", "description", "created_at", "updated_at"),
    )
