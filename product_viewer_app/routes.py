from flask import render_template, redirect, url_for, request
from product_viewer_app import app, db
from .helpers import save_file
from .forms import UploadForm

import os

@app.route("/", methods=["GET", "POST"])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        save_file(form)
        return redirect(url_for("products"))
    return render_template("index.html", title="ACME Inc. Product Viewer", form=form)

@app.route("/products", methods=["GET", "POST"])
def products():
    return render_template("products.html")