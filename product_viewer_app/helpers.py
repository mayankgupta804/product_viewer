from werkzeug.utils import secure_filename
from flask import flash
from product_viewer_app import app, db
from .models import FileMetaData

import os

def is_name_unique(filename):
    csv_object = db.session.query(FileMetaData).filter_by(filename=filename).one_or_none()
    if csv_object is None:
        return True
    return False    

def save_file(form):
    filename = secure_filename(form.file.data.filename)
    file = form.file.data
    upload_folder = app.config.get("UPLOADED_CSV_DEST")
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    upload_path = os.path.join(app.config.get("UPLOADED_CSV_DEST"), filename)
    file.save(upload_path)
    name = filename.split(".")[0]
    file_id = save_file_meta_data(form, upload_path, name)
    flash("{} uploaded successfully".format(filename))
    return file_id

def save_file_meta_data(form, upload_path, filename):
    file = FileMetaData()
    file.path = upload_path
    file.filename = filename
    db.session.add(file)
    db.session.commit()
    file_id = file.id
    return file_id