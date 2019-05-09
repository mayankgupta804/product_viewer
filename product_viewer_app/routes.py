from flask import render_template, redirect, url_for, request
from product_viewer_app import app, db
from .helpers import save_file
from .forms import UploadForm
from .celery_tasks import save_product_data

import os

@app.route("/", methods=["GET", "POST"])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        file_id = save_file(form)
        return redirect(url_for("products", id=file_id))
    return render_template("index.html", title="ACME Inc. Product Viewer", form=form)

@app.route("/products/<int:id>", methods=["GET", "POST"])
def products(id):
    save_product_data.delay(id)
    return render_template("products.html")