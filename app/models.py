from app import db
from flask_login import UserMixin
from datetime import datetime


class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(128), nullable=False)
    answer = db.Column(db.String(128), nullable=False)



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    scores = db.relationship('Score', backref='user', lazy=True)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    total_correct = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Score(user_id: {self.user_id}, date: {self.date}, total_correct: {self.total_correct})"