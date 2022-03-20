from flask import Blueprint

from project import app

frontend = Blueprint(
    "frontend", __name__, static_folder="../static/frontend", static_url_path="/"
)


@frontend.route("/admin")
@frontend.route("/admin/<path:path>")
@frontend.route("/login")
@frontend.route("/news")
@frontend.route("/news/<path:path>")
@frontend.route("/places")
@frontend.route("/places/<path:path>")
@frontend.route("/user/<path:path>")
def index(path=None):  # pragma: no cover
    return frontend.send_static_file("index.html")


app.register_blueprint(frontend)
