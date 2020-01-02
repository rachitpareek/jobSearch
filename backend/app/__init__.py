from flask import Flask

UPLOAD_FOLDER = './app/analysis'
ALLOWED_EXTENSIONS = {'csv', 'pdf'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import routes