"""
This module defines the authentication routes for the application.
"""

from flask import request
from flask_restx import Namespace, Resource, fields
from marshmallow import ValidationError
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from src.schemas import user_schema, user_auth_schema
from src import db
from src.models import User, TokenBlocklist


auth_ns = Namespace('auth', description='Authentication operations')

register_model = auth_ns.model(
    'RegisterUser',
    {
        'username': fields.String(required=True, description='Username'),
        'email': fields.String(required=True, description='Email address'),
        'password': fields.String(required=True, description='Password'),
        'bio': fields.String(description='User bio'),
        'profile_picture': fields.String(description='Profile picture URL'),
    },
)

login_model = auth_ns.model(
    'Login',
    {
        'username': fields.String(required=True, description='Username'),
        'password': fields.String(required=True, description='Password'),
    },
)

refresh_token_model = auth_ns.model(
    'RefreshToken',
    {
        'access_token': fields.String(required=True, description='Refresh token'),
    },
)

auth_response_model = auth_ns.model(
    'AuthResponse',
    {
        'access_token': fields.String(description='Access token'),
        'refresh_token': fields.String(description='Refresh token'),
        'user': fields.Raw(description='User information'),
    },
)

register_response_model = auth_ns.model(
    'RegisterResponse',
    {
        'message': fields.String(description='Success message'),
        'user': fields.Raw(description='User information'),
    },
)


@auth_ns.route('/register')
class Register(Resource):
    """
    Class for user registration.
    """

    @auth_ns.expect(register_model)
    @auth_ns.response(201, 'User registered successfully', register_model)
    @auth_ns.response(400, 'Bad request')
    @auth_ns.response(409, 'User already exists')
    def post(self):
        """
        Register a new user.

        :param: {
            'username': str,
            'email': str,
            'password': str,
            'bio': str,
            'profile_picture': str
        }

        :return: {
            "access_token": str,
            "refresh_token": str,
            "user": dict
        }
        """
        try:
            user_data = user_schema.load(request.json)
        except ValidationError as err:
            return {"error": err.messages}, 422

        # Checks if the user already exists (email or username)
        existing_username, existing_email = (
            User.query.filter_by(username=user_data["username"]).first(),
            User.query.filter_by(email=user_data["email"]).first(),
        )

        if existing_username or existing_email:
            return {"error": "User already exists"}, 409

        # Create a new user
        new_user = User(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
            bio=user_data.get("bio"),
            profile_picture=user_data.get("profile_picture"),
        )
        db.session.add(new_user)
        db.session.commit()

        # Generate access and refresh tokens
        access_token = create_access_token(identity=new_user.user_id)
        refresh_token = create_refresh_token(identity=new_user.user_id)

        # Create the response
        user = user_auth_schema.dump(new_user)

        return user_auth_schema.dump({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user,
        }), 201
        # return {
        #     "message": "User registered successfully",
        #     "user": user,
        #     "access_token": access_token,
        #     "refresh_token": refresh_token,
        # }, 201


@auth_ns.route('/login')
class Login(Resource):
    """
    Class for user login.
    """

    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'User logged in successfully', auth_response_model)
    @auth_ns.response(401, 'Invalid credentials')
    def post(self):
        """
        Log in a user.

        :param: {
            'username': str,
            'password': str
        }

        :return: {'access_token': str, 'refresh_token': str, 'user': dict}
        """
        data = request.json
        username = data.get("username", None)
        password = data.get("password", None)
        email = data.get("email", None)

        if not password:
            return {"error": "Password is required"}, 400

        if not (username or email):
            return {"error": "Username or email is required"}, 400

        # Find the user by username or email
        if username:
            user = db.session.query(User).filter_by(username=username).first()
        else:
            user = db.session.query(User).filter_by(email=email).first()

        # Check if the user exists and verify the password
        if not user or not user.verify_password(password):
            return {"error": "Invalid credentials"}, 401

        # Generate access and refresh tokens
        access_token = create_access_token(identity=user.user_id)
        refresh_token = create_refresh_token(identity=user.user_id)

        return user_auth_schema.dump({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user,
        }), 200


@auth_ns.route('/refresh')
class Refresh(Resource):
    """
    Class for refreshing access tokens.
    """

    @jwt_required(refresh=True)
    @auth_ns.expect(refresh_token_model)
    @auth_ns.response(200, 'Access token refreshed successfully', refresh_token_model)
    @auth_ns.response(401, 'Invalid refresh token')
    def post(self):
        """
        Refresh the access token.

        :return: {'access_token': str, 'refresh_token': str}
        """

        current_user_id = get_jwt_identity()
        user = db.session.get(User, current_user_id)

        if not user:
            return {"error": "User not found"}, 404

        # Generate new access and refresh tokens
        access_token = create_access_token(identity=user.user_id)
        # refresh_token = create_refresh_token(identity=user.user_id)

        return {
            "access_token": access_token,
            # "refresh_token": refresh_token,
        }, 200


@auth_ns.route('/logout')
class Logout(Resource):
    """
    Class for user logout.
    """

    @jwt_required()
    @auth_ns.response(200, 'User logged out successfully')
    def post(self):
        """
        Log out a user.

        :return: {'message': str}
        """
        jwt_payload = get_jwt()
        jti = jwt_payload["jti"]

        # Add the jti to the blacklist
        blacklisted_token = TokenBlocklist(jti=jti)

        db.session.add(blacklisted_token)
        db.session.commit()

        return {"message": "User logged out successfully"}, 200


@auth_ns.route('/me')
class UserInfo(Resource):
    """
    Class for getting user information.
    """

    @jwt_required()
    @auth_ns.response(200, 'User information retrieved successfully')
    @auth_ns.response(404, 'User not found')
    def get(self):
        """
        Get the current user's information.

        :return: {'user': dict}
        """
        current_user_id = get_jwt_identity()
        user = db.session.get(User, current_user_id)

        if not user:
            return {"error": "User not found"}, 404

        user_data = user_schema.dump(user)

        return {"user": user_data}, 200
