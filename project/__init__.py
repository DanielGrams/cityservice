import os

from flask import Blueprint, Flask, render_template, send_from_directory
from flask_cors import CORS
from flask_gzip import Gzip
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SERVER_NAME"] = os.getenv("SERVER_NAME")

# Gzip
gzip = Gzip(app)

# cors
cors = CORS(
    app,
    resources={r"/api/*"},
)

# Create db
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# API Resources
import project.api

# Command line
import project.cli.scrape

if os.getenv("TESTING", False):  # pragma: no cover
    import project.cli.test

# API
from project.api import RestApi

frontend = Blueprint(
    "frontend", __name__, static_folder="static/frontend", static_url_path="/"
)


@frontend.route("/news")
def news():  # pragma: no cover
    return frontend.send_static_file("index.html")


app.register_blueprint(frontend)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/impressum")
def impressum():
    return render_template("impressum.html")


@app.route("/datenschutz")
def datenschutz():
    return render_template("datenschutz.html")


media_path = os.path.join(app.root_path, "media")


@app.route("/media/<path:path>", methods=["GET"])
def serve_file_in_dir(path):
    return send_from_directory(media_path, path)


if __name__ == "__main__":  # pragma: no cover
    app.run()
