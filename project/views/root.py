import os.path

from flask import render_template, send_from_directory

from project import app


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
