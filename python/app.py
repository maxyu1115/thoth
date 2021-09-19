import _thread

from flask import Flask, request, send_from_directory, jsonify, flash
from werkzeug.utils import secure_filename
import json
import sys
import os

import whooshWrapper
import util
import thoth_engine

# Create public directory at startup.
from python.pipeline import Pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
publicDirectory = os.path.join(BASE_DIR, "storage")
if not os.path.exists(publicDirectory):
    os.makedirs(publicDirectory)


app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = publicDirectory
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mpeg', 'flv', 'wmv'}

searcher = whooshWrapper.WhooshWrapper(util.DirectoryLocator(app.config['UPLOAD_FOLDER']))

pipelines = dict()

directory_locator = util.DirectoryLocator(publicDirectory)


@app.route("/search", methods=["GET"])
def search():
    phrase = request.args.get('phrase')
    return json.dumps(searcher.searchWhoosh(phrase))


@app.route("/storage/<path:path>", methods=["GET"])
def get_file(path):
    return send_from_directory(publicDirectory, path)


@app.route("/upload_video", methods=["POST"])
def upload_video():
    try:
        if 'file' not in request.files:
            response = {"error": 'No file!'}
            return json.dumps(response)
        file = request.files['file']
        if not _allowed_file(file.filename):
            response = {"error": 'Invalid video file!'}
            return json.dumps(response)
        else:
            filename = secure_filename(file.filename)
            filepath = directory_locator.makeJsonPathname(filename)
            file.save(filepath)
            flash("Successfully uploaded video to ", filepath)
            _thread.start_new_thread(_process_video, (filename,))
            return {"filepath": filepath}
    except Exception:
        response = {"error": str(sys.exc_info()[1])}
    return json.dumps(response)


@app.route("/directory-data/<path:path>", methods=["GET"])
def get_directory_data(path):
    return ""


@app.route("/status/<path:path>", methods=["GET"])
def get_status(path):
    progress = total = 0
    pipeline = pipelines.get(directory_locator.makeJsonPathname(path))
    if pipeline is not None:
        progress, total = pipeline.getProgress()
    return json.dumps({"progress": progress, "total": total})


def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


def _process_video(video_name: str):
    # video_name: file name of video
    locator = util.FileLocator(video_name, directory_locator.output_path)
    pipeline = thoth_engine.createPipeline("animated")
    pipelines[video_name] = pipeline

    pipeline.processVideo(locator)


if __name__ == "__main__":
    app.run(debug=True)
