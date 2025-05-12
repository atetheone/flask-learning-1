from src import ma
from src.models import Post, PostVisibility
from marshmallow import fields, validate
from src.schemas import UserProfileSchema


class PostSchema(ma.SQLAlchemyAutoSchema):
    """
    Post schema for serialization and deserialization of Post objects.
    """

    class Meta:
        """
        Meta class for PostSchema.
        """

        model = Post
        ordered = True

    post_id = ma.auto_field(dump_only=True)
    content = fields.String(required=True, validate=validate.Length(min=1, max=5000))
    visibility = fields.String(
        required=True,
        validate=validate.OneOf(
            [
                PostVisibility.PUBLIC,
                PostVisibility.FOLLOWERS,
                PostVisibility.PRIVATE,
            ]
        ),
    )
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = ma.auto_field(dump_only=True)

    # Computed fields
    likes_count = fields.Method("get_likes_count", dump_only=True)
    comments_count = fields.Method("get_comments_count", dump_only=True)

    def get_likes_count(self, obj):
        """
        Get the count of likes for the post.
        """
        return obj.likes.count()

    def get_comments_count(self, obj):
        """
        Get the count of comments for the post.
        """
        return obj.comments.count()

    is_liked = fields.Boolean(dump_only=True)

    def get_is_liked(self, obj):
        """
        Get the like status of the post for the current user.
        """
        current_user = self.context.get("current_user")
        if not current_user:
            return False
        return obj.likes.filter_by(user_id=current_user.user_id).first() is not None

    authors = fields.Nested(UserProfileSchema, dump_only=True, many=True)

    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("posts.get_post", post_id="<post_id>"),
            "comments": ma.URLFor("posts.get_comments", post_id="<post_id>"),
            "likes": ma.URLFor("posts.get_likes", post_id="<post_id>"),
        }
    )


class PostCreateSchema(ma.Schema):
    """
    Schema for creating a new post.
    """

    content = fields.String(required=True, validate=validate.Length(min=1, max=5000))
    visibility = fields.String(
        required=True,
        validate=validate.OneOf(
            [
                PostVisibility.PUBLIC,
                PostVisibility.FOLLOWERS,
                PostVisibility.PRIVATE,
            ]
        ),
        default=PostVisibility.PUBLIC,
    )
