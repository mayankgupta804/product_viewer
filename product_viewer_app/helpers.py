from werkzeug.utils import secure_filename
from flask import flash
from product_viewer_app import app, db
from .models import Product, FileMetaData

import os

def save_file(form):
    filename = secure_filename(form.file.data.filename)
    file = form.file.data
    upload_folder = app.config.get("UPLOADED_CSV_DEST")
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    upload_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), filename)
    file.save(upload_path)
    save_file_meta_data(form, upload_path, filename)
    flash("{} uploaded successfully".format(filename))

def save_file_meta_data(form, upload_path, filename):
    file = FileMetaData()
    file.name = form.name.data
    file.description = form.description.data
    file.path = upload_path
    file.filename = filename
    db.session.add(file)
    db.session.commit()