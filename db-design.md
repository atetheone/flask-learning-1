# Database design of the social media API

## The tables

### Users table

- **user_id** (Primary Key, Integer, Auto Increment): Unique identifier for each user.
- **username** (String, Unique): The username of the user.
- **email** (String, Unique): The email address of the user.
- **password_hash** (String): The hashed password of the user.
- **created_at** (DateTime): The date and time when the user was created.
- **updated_at** (DateTime): The date and time when the user was last updated.
- **is_active** (Boolean): Indicates if the user account is active.

### Posts table

- **post_id** (Primary Key, Integer, Auto Increment): Unique identifier for each post.
- **user_id** (Foreign Key, Integer): The ID of the user who created the post.
- **content** (Text): The content of the post.
- **created_at** (DateTime): The date and time when the post was created.
- **updated_at** (DateTime): The date and time when the post was last updated.

### Comments table

- **comment_id** (Primary Key, Integer, Auto Increment): Unique identifier for each comment.
- **post_id** (Foreign Key, Integer): The ID of the post to which the comment belongs.
- **user_id** (Foreign Key, Integer): The ID of the user who created the comment.
- **content** (Text): The content of the comment.
- **created_at** (DateTime): The date and time when the comment was created.
- **updated_at** (DateTime): The date and time when the comment was last updated.
- **is_active** (Boolean): Indicates if the comment is active.
- **is_deleted** (Boolean): Indicates if the comment is deleted.

<!-- Optional: Add more tables for likes, shares, etc. -->
### Follows table

- **follower_id** (Foreign Key, Integer): The ID of the user who is following.
- **followed_id** (Foreign Key, Integer): The ID of the user who is being followed.
- **created_at** (DateTime): The date and time when the follow relationship was created.
- **is_active** (Boolean): Indicates if the follow relationship is active.
- **is_blocked** (Boolean): Indicates if the follow relationship is blocked.