from flask import Blueprint

from project import app

frontend = Blueprint(
    "frontend", __name__, static_folder="../static/frontend", static_url_path="/"
)


@frontend.route("/news")
def news():  # pragma: no cover
    return frontend.send_static_file("index.html")


@frontend.route("/profile")
def profile():  # pragma: no cover
    return frontend.send_static_file("index.html")


@frontend.route("/admin")
def admin():  # pragma: no cover
    return frontend.send_static_file("index.html")


@frontend.route("/login")
def login():  # pragma: no cover
    return frontend.send_static_file("index.html")


app.register_blueprint(frontend)
