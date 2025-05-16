from src import ma
from src.models import User
from marshmallow import fields, validate, validates, ValidationError, post_dump
import re


class UserSchema(ma.SQLAlchemyAutoSchema):
    """
    User schema for serialization and deserialization of User objects.
    """

    class Meta:
        """
        Meta class for UserSchema."""

        model = User
        ordered = True
        exclude = ("password",)  # Exclude password from serialization

    user_id = ma.auto_field(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(
        required=True, load_only=True, validate=validate.Length(min=8)
    )
    email = fields.Email(required=True)
    role = fields.String(dump_only=True)
    bio = fields.String()
    is_active = fields.Boolean(dump_only=True)
    is_verified = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    # Computed fields
    followers_count = fields.Method("get_followers_count", dump_only=True)
    following_count = fields.Method("get_following_count", dump_only=True)

    def get_followers_count(self, obj):
        """
        Get the count of followers for the user.
        """
        return obj.get_followers_count()

    def get_following_count(self, obj):
        """
        Get the count of users the user is following.
        """
        return obj.get_following_count()

    # Username validation
    @validates("username")
    def validate_username(self, value):
        """
        Validate the username to ensure it contains only
        alphanumeric characters and underscores.
        """
        pattern = r"^[a-zA-Z0-9_]+$"
        if not re.match(pattern, value):
            raise ValidationError(
                "Username must contain only letters," "numbers and underscores."
            )

        # Check if the username is already taken
        existing_user = User.query.filter_by(username=value).first()
        if existing_user and existing_user.user_id != self.context.get("user_id"):
            raise ValidationError("Username is already taken.")

    # Validation for email uniqueness
    @validates("email")
    def validate_email(self, value):
        """
        Validate the email to ensure it is unique.
        """
        # Check if the email is already taken
        existing_user = User.query.filter_by(email=value).first()
        if existing_user and existing_user.user_id != self.context.get("user_id"):
            raise ValidationError("Email is already taken.")

    # Add links for HATEOAS: Hypermedia as the Engine of Application State
    @post_dump
    def format_links(self, data, **kwargs):
        """
        Format the links for the user schema.
        """
        if "user_id" in data:
            data["_links"] = {
                "self": f"/users/{data['user_id']}",
                "posts": f"/users/{data['user_id']}/posts",
                "followers": f"/users/{data['user_id']}/followers",
                "following": f"/users/{data['user_id']}/following",
            }
        return data


class UserAuthSchema(ma.Schema):
    """
    User authentication schema for login and registration.
    """

    access_token = fields.String(required=True)
    refresh_token = fields.String(required=True)
    user = ma.Nested(UserSchema)


class UserProfileSchema(ma.SQLAlchemyAutoSchema):
    """
    User profile schema for serialization and deserialization of User objects.
    """

    class Meta:
        """
        Meta class for UserProfileSchema."""

        model = User
        ordered = True

    user_id = ma.auto_field(dump_only=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    bio = fields.String()
    profile_picture = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    followers_count = fields.Method("get_followers_count", dump_only=True)
    following_count = fields.Method("get_following_count", dump_only=True)
    is_following = fields.Method("get_is_following", dump_only=True)

    def get_followers_count(self, obj):
        """
        Get the count of followers for the user.
        """
        return obj.get_followers_count()

    def get_following_count(self, obj):
        """
        Get the count of users the user is following.
        """
        return obj.get_following_count()

    def get_is_following(self, obj):
        """
        Check if the authenticated user is following the user.
        """
        # Assuming `self.context` contains the authenticated user
        current_user = self.context.get("current_user")
        if current_user:
            return current_user.is_following(obj)
        return False

    @post_dump
    def format_links(self, data, **kwargs):
        """
        Format the links for the user profile schema.
        """
        if "user_id" in data:
            data["_links"] = {
                "self": f"/users/{data['user_id']}",
                "followers": f"/users/{data['user_id']}/followers",
                "following": f"/users/{data['user_id']}/following",
                "posts": f"/users/{data['user_id']}/posts",
            }
        return data
