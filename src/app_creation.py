from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow.exceptions import MarshmallowError
from werkzeug.exceptions import HTTPException

from src.config import Config
from src.exceptions import ApiException

db = SQLAlchemy()
migrate = Migrate(compare_type=True)
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from src.api import bp as api_bp
    from src import error_handlers

    app.register_blueprint(api_bp, url_prefix='/api')

    app.register_error_handler(ApiException, error_handlers.handle_api_exception)
    app.register_error_handler(MarshmallowError, error_handlers.handle_marshmallow_exception)
    app.register_error_handler(HTTPException, error_handlers.handle_http_exception)
    app.register_error_handler(Exception, error_handlers.handle_server_exception)

    return app
