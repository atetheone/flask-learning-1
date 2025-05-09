from datetime import datetime, timezone
from app import db


class Author(db.Model):
    """
    Represents an author in the database.

    Attributes:
        author_id (int): The primary key for the author.
        first_name (str): The first name of the author.
        last_name (str): The last name of the author.
        birth_date (date): The birth date of the author (optional).
        biography (str): The biography of the author (optional).
        created_at (datetime): The timestamp when the author was created.
        updated_at (datetime): The timestamp when the author was last updated.
    """

    __tablename__ = "authors"

    author_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    biography = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    # Relationships
    books = db.relationship("Book", back_populates="author", lazy="dynamic")

    # def __repr__(self):
    #     return f"<Author {self.first_name} {self.last_name}>"
