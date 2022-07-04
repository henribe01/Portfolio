from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'admin.login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from portfolio.main import bp as main_bp
    app.register_blueprint(main_bp)

    from portfolio.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    return app
