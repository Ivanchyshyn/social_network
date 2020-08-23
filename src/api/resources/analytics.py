from datetime import datetime

from flask import request
from flask_restful import Resource
from sqlalchemy import func

from src.api.utils import get_api_result_structure
from src.exceptions import ApiException
from src.models import UserPostLikes


class AnalyticsView(Resource):
    DATE_FMT = '%Y-%m-%d'

    def get(self):
        result = get_api_result_structure()
        date_from, date_to = request.args.get('date_from'), request.args.get('date_to')
        self.validate_dates(date_from, date_to)

        agg_data = UserPostLikes.query.with_entities(UserPostLikes.created, func.count(UserPostLikes.created)).filter(
            UserPostLikes.created.between(date_from, date_to)
        ).group_by(UserPostLikes.created).order_by(UserPostLikes.created).all()

        data = {}
        for date, count in agg_data:
            data[str(date)] = count

        result['data'] = data
        return result

    def validate_dates(self, date_from, date_to):
        try:
            date_from = datetime.strptime(date_from, self.DATE_FMT)
            date_to = datetime.strptime(date_to, self.DATE_FMT)
            if date_from > date_to:
                raise ApiException("'date_from' is bigger than 'date_to'")

        except (ValueError, TypeError):
            raise ApiException('Invalid date')
