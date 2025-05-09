from datetime import datetime, timezone
from app import db

# Assoc table many-to-many books and categories
book_categories = db.Table(
    "book_categories",
    db.Column("book_id", db.Integer, db.ForeignKey("books.book_id"), primary_key=True),
    db.Column(
        "category_id",
        db.Integer,
        db.ForeignKey("categories.category_id"),
        primary_key=True,
    ),
)


# Main table class
class Category(db.Model):
    """
    Represents a category in the database.

    Attributes:
        category_id (int): The unique identifier for the category.
        name (str): The name of the category.
        description (str): A description of the category.
        updated_at (datetime): The timestamp when the category was last
            updated.
        created_at (datetime): The timestamp when the category was created.
        books (list): A list of books associated with the category.
    """

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # def __repr__(self):
    #     return f"<Category {self.name}>"

    # def to_dict(self):
    #     """
    #     Converts the Category object into a dictionary representation.

    #     Returns:
    #         dict: A dictionary containing the category's details.
    #     """
    #     return {
    #         "category_id": self.category_id,
    #         "name": self.name,
    #         "description": self.description,
    #         "updated_at": self.updated_at,
    #         "created_at": self.created_at,
    #     }

    # Relationship
    books = db.relationship(
        "Book", secondary=book_categories, back_populates="categories"
    )
