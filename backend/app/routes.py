import os
import time
import json
from app import app, tester, analysis, ALLOWED_EXTENSIONS
from flask import render_template, jsonify, request, redirect
from werkzeug.utils import secure_filename

FILENAME = ""

@app.route('/')
@app.route('/index')
def index():
    show = tester.run()
    if isinstance(show, str):
        return render_template('index.html', no_table=True)
    return render_template('index.html', no_table=False, tables=[show.to_html(classes='data', header="true")], titles=show.columns.values)
	
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
        return redirect("/")
    elif request.method == 'GET':
        return render_template('upload.html')

@app.route('/analyze')
def analyze():
    results = analysis.run()
    if not results:
        return "The table uploaded didn't have the correct columns for analysis." 
    return render_template('analysis.html', results=results)

# delete from git repo
# clean stuff up
# tag data
# design api
# delete node app, rename flask one