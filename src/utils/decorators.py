from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask import jsonify
from functools import wraps
from src import db
from src.models import User, UserRole


def role_required(role=None):
    """
    Decorator to check if the user has a specific role.
    If role is None, only checks if user exists (authenticated).
    """

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            user = db.session.get(User, identity["user_id"])
            if not user or (role and user.role != role):
                required = f"{role} access required" if role else "User access required"
                return jsonify({"error": required}), 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def admin_required():
    return role_required(UserRole.ADMIN)


def moderator_required():
    return role_required(UserRole.MODERATOR)


def user_required():
    return role_required()
