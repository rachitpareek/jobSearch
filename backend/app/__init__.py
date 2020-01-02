from flask import Flask
import os

UPLOAD_FOLDER = './app/analysis'
ALLOWED_EXTENSIONS = {'csv', 'pdf'}

app = Flask(__name__, static_folder='templates/static',)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import routes