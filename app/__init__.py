from flask import Flask


def create_app():
    app = Flask(__name__, static_url_path="/static")
    with app.app_context():
        from .views import home

    return app
