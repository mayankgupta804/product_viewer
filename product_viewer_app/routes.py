from flask import render_template, flash, redirect, url_for, request
from product_viewer_app import app, db
from werkzeug.utils import secure_filename
from .forms import UploadForm

import os

@app.route("/", methods=["GET", "POST"])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.name.data
        filename = secure_filename(form.file.data.filename)
        file = form.file.data
        upload_folder = app.config.get("UPLOADED_CSV_DEST")
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        file.save(os.path.join(app.config.get("UPLOADED_CSV_DEST"), filename))
        return redirect(url_for("products"))
    return render_template("index.html", title="ACME Inc. Product Viewer", form=form)

@app.route("/products", methods=["GET", "POST"])
def products():
    return render_template("products.html")