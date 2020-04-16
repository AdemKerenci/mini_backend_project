from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import CONFIG

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(CONFIG)

    db.init_app(app)

    from .views import base_bp

    app.register_blueprint(base_bp)

    return app
