from datetime import datetime

from flask_jwt_extended import create_access_token, create_refresh_token, decode_token, get_raw_jwt
from flask_jwt_extended.config import config

from src import db
from src.models import Token, User


def get_api_result_structure():
    result = {
        'result': True,
        'error': None,
        'data': None
    }
    return result


def set_error_result(data, msg):
    data['result'] = False
    data['error'] = msg
    return data


def create_access_refresh_tokens(identity):
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    add_tokens_to_database(access_token=access_token, refresh_token=refresh_token)
    data = {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }
    return data


def add_tokens_to_database(access_token, refresh_token):
    if not access_token or not refresh_token:
        return

    access_db = _add_token_to_database(access_token)
    refresh_db = _add_token_to_database(refresh_token)

    refresh_db.partner_token = access_db
    db.session.commit()


def change_access_token_for_refresh(access_token):
    if not access_token:
        return

    raw_jwt = get_raw_jwt()
    jti = raw_jwt['jti']
    user_uuid = raw_jwt[config.identity_claim_key]
    user_id = User.query.filter_by(public_id=user_uuid).first().id

    refresh_db = Token.query.filter_by(
        jti=jti, user_id=user_id, token_type='refresh',
    ).first()
    if not refresh_db:
        return

    access_db = _add_token_to_database(access_token)
    refresh_db.partner_token = access_db
    db.session.commit()


def _add_token_to_database(encoded_token):
    """
    Adds a new token to the database. It is not revoked when it is added.
    """
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']
    token_type = decoded_token['type']
    user_identity = decoded_token[config.identity_claim_key]
    expires = datetime.fromtimestamp(decoded_token['exp'])
    revoked = False

    user_id = User.query.filter_by(public_id=user_identity).first().id

    db_token = Token(
        jti=jti,
        token_type=token_type,
        user_id=user_id,
        expires=expires,
        revoked=revoked,
    )
    db.session.add(db_token)
    return db_token
