"""Book model for the database.
This module defines the Book class, which represents a book in the
"""

from datetime import datetime, timezone
from app import db


class Book(db.Model):
    """
    Represents a book in the database.

    Attributes:
        book_id (int): The primary key of the book.
        title (str): The title of the book.
        isbn (str): The ISBN of the book.
        publication_date (date): The publication date of the book.
        price (Decimal): The price of the book.
        stock (int): The stock quantity of the book.
        description (str): A description of the book.
        updated_at (datetime): The last updated timestamp.
        created_at (datetime): The creation timestamp.
        author_id (int): The foreign key to the author.
        publisher_id (int): The foreign key to the publisher.
    """

    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(20), nullable=False, unique=True)
    publication_date = db.Column(db.Date, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    description = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # def __repr__(self):
    #     return f"<Book {self.title}>"

    # def to_dict(self):
    #     """
    #     Converts the book instance to a dictionary.

    #     Returns:
    #         dict: A dictionary representation of the book.
    #     """
    #     return {
    #         "book_id": self.book_id,
    #         "title": self.title,
    #         "isbn": self.isbn,
    #         "publication_date": self.publication_date,
    #         "price": float(self.price),
    #         "stock": self.stock,
    #         "description": self.description,
    #         "updated_at": self.updated_at,
    #         "created_at": self.created_at,
    #         "author_id": self.author_id,
    #         "publisher_id": self.publisher_id,
    #     }
    author_id = db.Column(db.Integer, db.ForeignKey("authors.author_id"), nullable=False)
    publisher_id = db.Column(
        db.Integer, db.ForeignKey("publishers.publisher_id"), nullable=False
    )

    # Relationship
    author = db.relationship("Author", back_populates="books")
    publisher = db.relationship("Publisher", back_populates="books")
    categories = db.relationship(
        "Category", secondary="book_categories", back_populates="books"
    )
