from flask import request
from flask_restful import Resource

from src.api.utils import get_api_result_structure, create_access_refresh_tokens
from src.exceptions import ApiException
from src.models import User
from src.serializers import UserSchema


class SignIn(Resource):
    def post(self):
        result = get_api_result_structure()
        data = request.get_json(force=True, silent=True) or {}
        email, password = data.get('email'), data.get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            raise ApiException("User not found")

        data = create_access_refresh_tokens(identity=user)
        data['user'] = UserSchema().dump(user)
        result['data'] = data
        return result
