from datetime import datetime
from functools import wraps

from flask_jwt_extended import current_user

from src import db


def user_last_request(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if current_user is not None:
            current_user.last_request = datetime.utcnow()
            db.session.commit()
        return func(*args, **kwargs)

    return wrapped
