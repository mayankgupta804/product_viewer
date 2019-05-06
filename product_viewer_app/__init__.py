from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from logging.handlers import RotatingFileHandler
from flask_uploads import UploadSet, configure_uploads

import logging
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/product_viewer_app.log', maxBytes=10240, backupCount=10)   
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')) 
file_handler.setLevel(logging.INFO)  
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Starting App...')  

# Configure the csv files uploading via Flask-Uploads
csv = UploadSet('files', ('csv', ))
configure_uploads(app, csv)

from product_viewer_app import routes



