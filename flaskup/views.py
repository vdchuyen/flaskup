# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect, request, abort
from flask import send_file, make_response
from flaskup import app
from flaskup.utils import process_file, get_file_info

@app.route('/')
def show_upload_form():
    return render_template('show_upload_form.html')

@app.route('/upload-xhr', methods=['POST'])
def upload_file_xhr():
    try:
        infos = process_file(request)
    except Exception as e:
        return e, 400
    return url_for('show_uploaded_file', key=infos['key'])

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        infos = process_file(request)
    except Exception as e:
        return render_template('show_upload_form.html', error=e)
    return redirect(url_for('show_uploaded_file', key=infos['key'])) 

@app.route('/uploaded/<key>/')
def show_uploaded_file(key):
    try:
        infos = get_file_info(key)
    except IOError:
        abort(404)
    return render_template('show_uploaded_file.html', infos=infos)

@app.route('/get/<key>/')
def show_get_file(key):
    try:
        infos = get_file_info(key)
    except IOError:
        abort(404)
    return render_template('show_get_file.html', infos=infos)

@app.route('/get/<key>/<filename>')
def get_file(key, filename):
    try:
        infos = get_file_info(key)
    except IOError:
        abort(404)

    if not infos['filename'] == filename:
        abort(404)

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], infos['path'], filename)
    if not os.path.isfile(filepath):
        abort(404)

    filesize = str(os.path.getsize(filepath))
    response = make_response(send_file(filepath, as_attachment=True,
                             attachment_filename=filename))
    response.headers['Content-Length'] = filesize
    return response

