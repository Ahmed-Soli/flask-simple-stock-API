from functools import wraps

from flask import abort
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] == "ADMIN":
                return fn(*args, **kwargs)
            else:
                return abort(403, "Unauthorized")

        return decorator

    return wrapper