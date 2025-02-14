from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from Site import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(16), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete, delete-orphan")
    comments = db.relationship('Comment', backref='author', lazy=True, cascade="all, delete, delete-orphan")

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.secret_key)
        return s.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.secret_key)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.id}':'{self.username}', '{self.email}', {self.image_file})"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    is_updated = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete, delete-orphan")
    pictures = db.relationship('Picture', backref='pic_post', lazy=True, cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"Post('{self.id}':'{self.title}', '{self.date_posted}')"
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_commented = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    is_updated = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picture = db.Column(db.String(20), nullable=True, default="ImageIsNull")
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)