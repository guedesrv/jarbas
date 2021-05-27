# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask import Blueprint
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap

from . import views

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

# login variable initialization
login_manager = LoginManager()

# Email variable initialization
mail = Mail()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    #app.config.from_pyfile('config.py')

    app.config['MAIL_SERVER']='smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = 'a2ecdcdb404e2a'
    app.config['MAIL_PASSWORD'] = 'a5f048a0e7d90d'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    Bootstrap(app)
    mail.init_app(app)
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "Você precisa estar logado para acessar esta página."
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app