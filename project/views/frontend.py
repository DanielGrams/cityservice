from flask import Blueprint

from project import app

frontend = Blueprint(
    "frontend", __name__, static_folder="../static/frontend", static_url_path="/"
)


@frontend.errorhandler(404)
@frontend.route("/")
def index(path=None):  # pragma: no cover
    return frontend.send_static_file("index.html")


app.register_blueprint(frontend)
