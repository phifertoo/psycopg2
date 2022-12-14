"""Flask example."""
import os
from http import HTTPStatus

from flask import Flask, request
from flask import jsonify

from werkzeug.utils import secure_filename
"""
Author: James Campbell
Date: Mon May 23 16:26:36 2016
Date Updated: 2 July 2019
What is this code: An example Flask connection
Why?: For me to remember later
"""

app = Flask(__name__)
ALLOWED_EXTENSIONS = ["zip", "gz", "bz2"]


def allowed_filename(filename: str) -> bool:
    """Define allowed file extensions."""
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


@app.route("/")
def hello_world():
    """Hello world example."""
    return """\
        <!DOCTYPE html><head><title>Flask test</title></head>\
            <body style="font-family:monospace;">Hello, simply run\
            <pre style="color:blue;">curl -X POST localhost:6969/upload\
            -F file=@"assets/archive_name.tar.gz" -i</pre> to test from\
                 same folder you executed <pre style="color:blue;">python3\
                    flask-example.py</pre></body>
                    """


@app.route("/upload", methods=["POST"])
def upload_csv() -> str:
    """Upload CSV example."""
    submitted_file = request.files["file"]
    if submitted_file and allowed_filename(submitted_file.filename):
        filename = secure_filename(submitted_file.filename)
        directory = os.path.join(app.config["UPLOAD_FOLDER"])
        if not os.path.exists(directory):
            os.mkdir(directory)
        basedir = os.path.abspath(os.path.dirname(__file__))
        submitted_file.save(
            os.path.join(basedir, app.config["UPLOAD_FOLDER"], filename)
        )
        out = {
            "status": HTTPStatus.OK,
            "filename": filename,
            "message": f"{filename} saved successful.",
        }
        return jsonify(out)


if __name__ == "__main__":
    app.config["UPLOAD_FOLDER"] = "flaskme/"
    app.run(port=6969, debug=True)

# curl -X POST localhost:6969/upload -F file=@"assets/archive_name.tar.gz" -i
