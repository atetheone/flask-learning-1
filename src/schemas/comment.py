from src import ma
from src.models import Comment
from marshmallow import fields, validate


class CommentSchema(ma.SQLAlchemyAutoSchema):
    """
    Comment schema for serialization and deserialization of Comment objects.
    """

    class Meta:
        """
        Meta class for CommentSchema.
        """

        model = Comment
        ordered = True

    comment_id = ma.auto_field(dump_only=True)
    content = fields.String(required=True, validate=validate.Length(min=1, max=1000))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = ma.auto_field(dump_only=True)
    post_id = ma.auto_field(dump_only=True)
    parent_id = ma.auto_field()

    author = fields.Nested('UserProfileSchema', dump_only=True)
    replies = fields.List(fields.Nested('CommentSchema'), dump_only=True)

    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("comments.get_comment", comment_id="<comment_id>"),
            "post": ma.URLFor("posts.get_post", post_id="<post_id>"),
            "replies": ma.URLFor("comments.get_replies", comment_id="<comment_id>"),
        }
    )


class CommentCreateSchema(ma.Schema):
    """
    Schema for creating a new comment.
    """

    content = fields.String(required=True, validate=validate.Length(min=1, max=1000))
    parent_id = fields.Integer()
