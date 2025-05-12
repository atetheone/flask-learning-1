from src.schemas.user import UserSchema, UserAuthSchema, UserProfileSchema
from src.schemas.post import PostSchema, PostCreateSchema
from src.schemas.comment import CommentSchema, CommentCreateSchema


user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_auth_schema = UserAuthSchema()
user_profile_schema = UserProfileSchema()
user_profiles_schema = UserProfileSchema(many=True)

post_schema = PostSchema()
posts_schema = PostSchema(many=True)
post_create_schema = PostCreateSchema()

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
comment_create_schema = CommentCreateSchema()
