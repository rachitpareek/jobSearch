from flask import Flask
from flask_bootstrap import Bootstrap

UPLOAD_FOLDER = './app'
ALLOWED_EXTENSIONS = {'csv', 'pdf'}

app = Flask(__name__, static_folder='templates/static',)
Bootstrap(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import routes