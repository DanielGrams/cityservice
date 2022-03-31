import os.path

from flask import send_from_directory

from project import app

media_path = os.path.join(app.root_path, "media")


@app.route("/media/<path:path>", methods=["GET"])
def serve_file_in_dir(path):
    return send_from_directory(media_path, path)
