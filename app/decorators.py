from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user

from app.models import Permission


def permission_required(permission, redirect_endpoint='main.index'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                return redirect(url_for(redirect_endpoint))
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
