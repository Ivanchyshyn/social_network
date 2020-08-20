from src import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
