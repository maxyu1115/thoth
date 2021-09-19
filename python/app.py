from flask import Flask, request, send_from_directory, jsonify, flash
from werkzeug.utils import secure_filename
import json
import sys
import os

import whooshWrapper
import util


# Create public directory at startup.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
publicDirectory = os.path.join(BASE_DIR, "public")
if not os.path.exists(publicDirectory):
    os.makedirs(publicDirectory)

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = publicDirectory

searcher = whooshWrapper.WhooshWrapper(util.DirectoryLocator(app.config['UPLOAD_FOLDER']))


@app.route("/search", methods = ["GET"])
def search():
    phrase = request.args.get('phrase')
    return json.dumps(searcher.searchWhoosh(phrase))


@app.route("/storage/<path:path>", methods = ["GET"])
def get_file(path):
    return send_from_directory("public/", path)


@app.route("/upload_video", methods = ["POST"])
def upload_video():
    try:
        if 'file' not in request.files:
            print("YEET")
            # flash('No file part')
            return send_from_directory("public/", "your_file.txt")
        file = request.files['file']
        if file.filename == '':
            # flash('No image selected for uploading')
            return send_from_directory("public/", "your_file.txt")
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # print('upload_video filename: ' + filename)
            # flash('Video successfully uploaded and displayed below')
            return send_from_directory("public/", "your_file.txt")
        # response = Video.upload(FlaskAdapter(request),"/public/")
    except Exception:
        response = {"error": str(sys.exc_info()[1])}
    return json.dumps(response)


@app.route("/directory-data/<path:path>", methods = ["GET"])
def get_directory_data(path):
    return ""


@app.route("/status/<path:path>", methods = ["GET"])
def get_directory_data(path):
    return ""


app.run(debug=True)
