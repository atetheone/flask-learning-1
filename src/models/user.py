"""
Flask application factory for the project.
This module contains the create_app function that initializes the Flask application,
"""

from src import db
from datetime import datetime, timezone
from passlib.hash import pbkdf2_sha256 as sha256  # type: ignore


# User roles
class Role:
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class User(db.Model):
    """
    User model for the application.
    Represents a user in the system with various attributes and relationships.
    """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default=Role.USER)
    bio = db.Column(db.Text, nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    last_login = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    posts = db.relationship(
        "Post",
        backref="author",
        lazy='dynamic',
        cascade="all, delete-orphan"
    )
    comments = db.relashionship(
        "Comment",
        backref="author",
        lazy='dynamic',
        cascade="all, delete-orphan"
    )
    followers = db.relationship(
        "User",
        secondary="followers",
        primaryjoin=('User.user_id == Relationship.follower_id'),
        secondaryjoin=('User.user_id == Relationship.followed_id'),
        backref=db.backref("following", lazy="dynamic")
    )

    @property
    def password(self):
        """
        Prevents password from being accessed directly.
        """

        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        """
        Hashes the password using PBKDF2 SHA256 algorithm.
        """

        self.password_hash = sha256.hash(password)

    def verify_password(self, password):
        """
        Verifies the provided password against the stored password hash.
        """

        return sha256.verify(password, self.password_hash)

    def follow(self, user):
        """
        Follows a user.
        """

        if not self.is_following(user):
            from src.models.relationship import Relationship
            relationship = Relationship(
                follower_id=self.user_id,
                followed_id=user.user_id
            )
            db.session.add(relationship)

    def unfollow(self, user):
        """
        Unfollows a user.
        """

        if self.is_following(user):
            from src.models.relationship import Relationship
            relationship = Relationship.query.filter_by(
                follower_id=self.user_id,
                followed_id=user.user_id
            ).first()
            db.session.delete(relationship)

    def is_following(self, user):
        """
        Checks if the user is following another user.
        """
        from src.models.relationship import Relationship
        return Relationship.query.filter_by(
            follower_id=self.user_id,
            followed_id=user.user_id
        ).count() > 0

    def get_followers_count(self):
        """
        Returns the count of followers for the user.
        """

        from src.models.relationship import Relationship
        return Relationship.query.filter_by(followed_id=self.user_id).count()

    def get_following_count(self):
        """
        Returns the count of users the user is following.
        """

        from src.models.relationship import Relationship
        return Relationship.query.filter_by(follower_id=self.user_id).count()


class TokenBlocklist(db.Model):
    """
    Token blocklist model for JWT tokens.
    Used to store revoked tokens.
    """

    __tablename__ = "token_blocklist"

    token_id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @classmethod
    def add_to_blocklist(cls, jti):
        """
        Adds a token to the blocklist.
        """

        blacklisted_token = cls(jti=jti)
        db.session.add(blacklisted_token)
        db.session.commit()
        return blacklisted_token

    @classmethod
    def is_black_listed(cls, jti):
        """
        Checks if a token is blacklisted.
        """

        return cls.query.filter_by(jti=jti).first() is not None
