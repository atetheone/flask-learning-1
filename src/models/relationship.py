"""
This module defines the Relationship class, which represents a relationship
between two users in the social media application.
"""

from src import db
from datetime import datetime, timezone


class Relationship(db.Model):
    """
    Relationship model representing a follower-followed relationship between users.
    """

    __tablename__ = "relationships"

    follower_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Relationship {self.id}>"
