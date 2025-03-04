from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import dotenv_values

env_var = dotenv_values('.env')

from Site.config import Config




db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(Config_class=Config):
    
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from Site.users.routes import users
    from Site.posts.routes import posts
    from Site.comments.routes import comments
    from Site.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(comments)
    app.register_blueprint(main)

    return app