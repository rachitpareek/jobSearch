import os
from app import app, tester, ALLOWED_EXTENSIONS
from flask import render_template, jsonify, request
from werkzeug.utils import secure_filename

FILENAME = ""

@app.route('/')
@app.route('/index')
def index():
    return str(tester.run())
	
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if not f.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            return 'You must upload a .csv file!'
        global FILENAME
        FILENAME = f.filename
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File ' + FILENAME + ' uploaded successfully!' 
    elif request.method == 'GET':
        return render_template('upload.html')