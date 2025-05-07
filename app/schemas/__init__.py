"""
This module imports all the schemas used in the application."""

from app.schemas.author import AuthorSchema
from app.schemas.book import BookSchema, BookDetailsSchema
from app.schemas.publisher import PublisherSchema
from app.schemas.category import CategorySchema

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)
book_details_schema = BookDetailsSchema()

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

publisher_schema = PublisherSchema()
publishers_schema = PublisherSchema(many=True)
