from flask import Blueprint
from flask_restful import Api

bp = Blueprint('api', __name__)
rest = Api(bp)

from . import urls
