"""
This module defines the Comment class, which represents Comments table in the database.
"""

from src import db
from datetime import datetime, timezone


class Comment(db.Model):
    """
    Comment model representing a comment on a post.
    """

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Optional parent comment for nested comments
    parent_id = db.Column(db.Integer, db.ForeignKey("comments.comment_id"), nullable=True)

    # self referencing relationship for nested comments
    replies = db.relationship(
        "Comment",
        backref=db.backref("parent", remote_side=[comment_id]),
        lazy="dynamic",
    )

    def __repr__(self):
        return f"<Comment {self.comment_id}>"
