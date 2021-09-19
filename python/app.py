import _thread

from flask import Flask, request, send_from_directory, jsonify, flash
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json
import sys
import os
import glob
import multiprocessing

import whooshWrapper
import util
import thoth_engine

# Create public directory at startup.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
storageDirectory = os.path.join(BASE_DIR, "storage")
if not os.path.exists(storageDirectory):
    os.makedirs(storageDirectory)


app = Flask(__name__)
CORS(app, support_credentials=True)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = storageDirectory
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mpeg', 'flv', 'wmv'}

directory_locator = util.DirectoryLocator(storageDirectory)

searcher = whooshWrapper.WhooshWrapper(directory_locator)

pipelines = dict()


def getPipeline(filename: str):
    print(filename)
    print(pipelines)
    return pipelines.get(filename)


@app.route("/search", methods=["GET"])
def search():
    phrase = request.args.get('phrase')
    return json.dumps(searcher.searchWhoosh(phrase))


@app.route("/storage/<path:path>", methods=["GET"])
def get_file(path):
    return send_from_directory(storageDirectory, path)


@app.route("/upload-video", methods=["POST"])
def upload_video():
    vid_type = request.args.get('vid-type')
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
            filepath = directory_locator.makeFilePathname(filename)
            file.save(filepath)
            flash("Successfully uploaded video to ", filepath)
            process = multiprocessing.Process(target=_process_video, args=(filename, vid_type,))
            process.start()
            return {"filepath": filepath}
    except Exception:
        response = {"error": str(sys.exc_info()[1])}
    return json.dumps(response)

@app.route("/directory-data", methods=["GET"], defaults={'path': ''})
@app.route("/directory-data/", methods=["GET"], defaults={'path': ''})
@app.route("/directory-data/<path:path>", methods=["GET"])
def get_directory_data(path):
    file_lst = glob.glob(os.path.join(directory_locator.getOutputRoot(), path) + "/*")
    output = dict()
    for filename in file_lst:
        if "." in filename:
            output[filename] = dict()
    return output


@app.route("/status/<name>", methods=["GET"])
def get_status(name):
    progress = total = 0
    pipeline = getPipeline(name)
    if pipeline is not None:
        progress, total = pipeline.getProgress()
    return json.dumps({"progress": progress, "total": total})


def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


def _process_video(video_name: str, vid_type: str):
    # video_name: file name of video
    locator = util.FileLocator(video_name, directory_locator.output_path)
    pipeline = thoth_engine.createPipeline(vid_type)
    print("process video: ", video_name)
    pipelines[video_name] = pipeline

    pipeline.processVideo(locator)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    app.run(host="0.0.0.0", port=8000, debug=True)
