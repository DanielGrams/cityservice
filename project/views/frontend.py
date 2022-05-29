from flask import Blueprint, request

from project import app

frontend = Blueprint(
    "frontend", __name__, static_folder="../static/frontend", static_url_path="/"
)


@frontend.route("/")
def index(path=None):  # pragma: no cover
    return frontend.send_static_file("index.html")


@frontend.errorhandler(404)
def not_found(e):  # pragma: no cover
    if request.path.startswith("/api"):
        return "", 404

    return frontend.send_static_file("index.html")


app.register_blueprint(frontend)
