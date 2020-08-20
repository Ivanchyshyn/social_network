import datetime
import os

from dotenv import load_dotenv

load_dotenv(override=True)


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    HOST = os.getenv('HOST', 'http://localhost:5000')

    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_NAME = os.environ.get('DB_NAME', 'social')
    DB_USER = os.environ.get('DB_USER', 'social_user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'social_user')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secret')
    PROPAGATE_EXCEPTIONS = True

    _access_expire = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_IN_SECONDS', 3600))  # default - 1 hour
    _refresh_expire = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES_IN_SECONDS', 2592000))  # default - 30 days
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=_access_expire)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(seconds=_refresh_expire)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
