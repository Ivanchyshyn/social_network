from sqlalchemy.orm.exc import NoResultFound

from src import jwt
from src.api.utils import get_api_result_structure, set_error_result
from src.models import User, Token


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.public_id


@jwt.user_loader_callback_loader
def user_loader_callback(public_id):
    return User.query.filter_by(public_id=public_id).first()


@jwt.unauthorized_loader
def unauthorized_callback(callback):
    # No auth header
    result = get_api_result_structure()
    return set_error_result(result, msg="Bad Authorization header")


@jwt.user_loader_error_loader
def custom_user_loader_error(identity):
    result = get_api_result_structure()
    return set_error_result(result, msg="User not found")


@jwt.invalid_token_loader
def invalid_token(error_msg):
    result = get_api_result_structure()
    return set_error_result(result, msg="Invalid token")


@jwt.expired_token_loader
def token_expiration(token):
    result = get_api_result_structure()
    return set_error_result(result, msg="Token has expired"), 401


@jwt.revoked_token_loader
def revoked_token():
    result = get_api_result_structure()
    return set_error_result(result, msg="Token has been revoked"), 401


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    jti = decoded_token['jti']
    try:
        token = Token.query.filter_by(jti=jti).one()
        return token.revoked
    except NoResultFound:
        return True
