import pytz
from flask_jwt_extended import jwt_optional, current_user
from flask_restful import Resource

from src.api.utils import get_api_result_structure
from src.exceptions import ApiException
from src.models import User


class UserActivityView(Resource):
    method_decorators = [jwt_optional]

    def get(self, user_id=None):
        result = get_api_result_structure()
        last_login = last_request = None
        if user_id is None:
            user = current_user
        else:
            user = User.query.filter_by(public_id=user_id).first()
            if not user:
                raise ApiException('User not found')

        if user:
            last_login = user.last_login
            last_request = user.last_request

        result['data'] = {
            'last_login': self.format_date(last_login),
            'last_request': self.format_date(last_request),
        }
        return result

    @staticmethod
    def format_date(date):
        if date is None:
            return None

        date = date.replace(tzinfo=pytz.UTC)
        return date.isoformat()
