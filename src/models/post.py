from src import db
from datetime import datetime, timezone


class PostVisibility:
    """
    Enum for post visibility options.
    """

    PUBLIC = "public"
    FOLLOWERS = "followers"
    PRIVATE = "private"


class Post(db.Model):
    """
    Post model representing a user's post.
    """

    __tablename__ = "posts"

    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    visibility = db.Column(db.String(20), default=PostVisibility.PUBLIC)

    # Relationships
    comments = db.relationship(
        "Comment",
        backref="post",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    likes = db.relationship(
        "Like",
        backref="post",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Post {self.post_id}>"

    def is_visible_to(self, user):
        """
        Check if the post is visible to a given user based on the visibility setting.
        """

        if user.user_id == self.user_id:
            return True

        # Check visibility based on the visibility setting
        if self.visibility == PostVisibility.PUBLIC:
            return True
        elif self.visibility == PostVisibility.FOLLOWERS:
            return user.is_following(self.author)
        else:
            # Private visibility
            return False


class Like(db.Model):
    """
    Like model representing a user's like on a post.
    """

    __tablename__ = "likes"

    like_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Like {self.like_id}>"

    __table_args__ = (
        db.UniqueConstraint("user_id", "post_id", name="unique_like"),
    )

    # Relationships
    user = db.relationship("User", backref=db.backref("likes", lazy="dynamic"))


"""

Tables:
    - posts
        - post_id
        - user_id
        - content
        - created_at
        - updated_at
        - visibility
    - likes
        - like_id
        - user_id
        - post_id
        - created_at
    - comments
        - comment_id
        - user_id
        - post_id
        - content
        - created_at
        - updated_at
    - followers
        - follower_id
        - followed_id
        - created_at
    - relationships
        - follower_id
        - followed_id
        - created_at

"""
