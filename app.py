#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash, request, redirect, url_for

DEVELOPMENT_ENV  = True

app = Flask(__name__)

app_data = {
    "name":         "Thoth - A note taking web app",
    "description":  "HackRice 11",
    "author":       "thoth",
    "html_title":   "Thoth - A note taking web app",
    "project_name": "Starter Template",
    "keywords":     "flask, webapp, template, basic"
}


@app.route('/')
def index():
    return render_template('index.html', app_data=app_data)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


# @app.route('/about')
# def about():
#     return render_template('about.html', app_data=app_data)
#
#
# @app.route('/service')
# def service():
#     return render_template('service.html', app_data=app_data)
#
#
# @app.route('/contact')
# def contact():
#     return render_template('contact.html', app_data=app_data)


if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_ENV)