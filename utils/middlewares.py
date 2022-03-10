from functools import wraps
from flask import jsonify, session


def require_authentication(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if ('user' not in session):
            return "Unauthorized", 401
        return f(*args, **kwargs)
    return wrapper


def require_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if ('user' not in session):
            return "Unauthorized", 401
        if not session['user']['is_admin']:
            return "Forbidden", 403
        return f(*args, **kwargs)
    return wrapper


def api(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        result: tuple = f(*args, **kwargs)
        if result.__len__() == 2:
            response, status = result
        else:
            response, status = result, 200
        return jsonify(response), status
    return wrapper
