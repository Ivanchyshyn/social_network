import uuid
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from src import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Text, default=uuid.uuid4, unique=True, nullable=False)

    email = db.Column(db.String(256), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))

    password = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    last_login = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    last_request = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        if not self.password or not password:
            return False
        return check_password_hash(self.password, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Text, default=uuid.uuid4, unique=True, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    text = db.Column(db.Text)

    author = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))
    users_liked = db.relationship('User', secondary='user_post_likes', lazy='dynamic')

    @property
    def users_liked_count(self):
        return self.users_liked.count()


class UserPostLikes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'))

    __table_args__ = (db.UniqueConstraint('user_id', 'post_id'),)


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User')

    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.TIMESTAMP, nullable=False)

    # connect access and refresh tokens
    partner_token_id = db.Column(db.Integer, db.ForeignKey('token.id'))
    partner_token = db.relationship('Token', uselist=False, cascade="all, delete-orphan")
