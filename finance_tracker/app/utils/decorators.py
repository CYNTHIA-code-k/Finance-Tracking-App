from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify

def require_active_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        # Add logic to fetch user by ID and check if active
        # For now, we assume user is active for demonstration purposes
        return f(*args, **kwargs)
    return decorated_function
