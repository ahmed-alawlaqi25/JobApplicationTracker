from flask import Flask, session
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("secret_key")
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app
