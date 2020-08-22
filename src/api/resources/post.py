from flask import request
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError

from src import db
from src.api.utils import get_api_result_structure
from src.exceptions import ApiException
from src.models import Post
from src.serializers import PostSchema


class PostView(Resource):
    method_decorators = [jwt_required]

    def get(self, post_id=None):
        result = get_api_result_structure()
        if post_id is None:
            posts = Post.query.all()
            data = PostSchema().dump(posts, many=True)
        else:
            post = self.get_post_instance(post_id)
            data = PostSchema().dump(post)

        result['data'] = data
        return result

    def post(self, post_id=None, action=None):
        post_actions = {
            None: self.create_post,
            'like': self.like_post,
            'unlike': self.unlike_post,
        }

        result = get_api_result_structure()
        post_data = request.get_json(force=True, silent=True) or {}

        post_instance = None
        if post_id is not None:
            post_instance = self.get_post_instance(post_id)

        if action in post_actions:
            instance = post_actions[action](post_data, post_instance)
        else:
            raise ApiException("Invalid action")

        result['data'] = PostSchema().dump(instance)
        return result

    def get_post_instance(self, post_id):
        post = Post.query.filter_by(public_id=post_id).first()
        if not post:
            raise ApiException('Post not found')
        return post

    def create_post(self, data, instance):
        valid_data = PostSchema().load(data)
        instance = Post(**valid_data)
        current_user.posts.append(instance)

        db.session.commit()
        return instance

    def like_post(self, data, instance):
        instance.users_liked.append(current_user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return instance

    def unlike_post(self, data, instance):
        instance.users_liked.remove(current_user)
        try:
            db.session.commit()
        except StaleDataError:
            db.session.rollback()
        return instance
