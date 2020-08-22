from flask import request
from flask_restful import Resource

from src import db
from src.api.utils import get_api_result_structure, create_access_refresh_tokens
from src.exceptions import ApiException
from src.models import User
from src.serializers import UserSchema


class SignUpView(Resource):
    def post(self):
        result = get_api_result_structure()
        post_data = request.get_json(force=True, silent=True) or {}
        valid_data = UserSchema().load(post_data)

        email, password = valid_data.pop('email'), valid_data.pop('password')
        if User.query.filter_by(email=email).first():
            raise ApiException("User already exists")

        user = User(email=email, **valid_data)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        data = create_access_refresh_tokens(identity=user)
        data['user'] = UserSchema().dump(user)
        result['data'] = data
        return result
