from app import db
from datetime import datetime, timezone


class Publisher(db.Model):
    __tablename__ = "publishers"

    publisher_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    website = db.Column(db.String(200), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    updated_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationship
    books = db.relationship("Book", back_populates="publisher", lazy="dynamic")

    def __repr__(self):
        return f"<Publisher {self.name}"
