"""
This file imports all the models used in the application.
"""

from src.models.user import User, Role, TokenBlocklist
from src.models.post import Post, Like, PostVisibility
from src.models.comment import Comment
from src.models.relationship import Relationship

_ = (
    User,
    Post,
    Like,
    PostVisibility,
    Comment,
    Relationship,
    TokenBlocklist,
    Role,
)  # noqa: F841 # to avoid unused import warnings
