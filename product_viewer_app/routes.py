from product_viewer_app import app, db
from flask import render_template, flash, redirect, url_for, request

from .forms import UploadForm

@app.route("/", methods=["GET", "POST"])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        flash("Upload success")
        return redirect(url_for("products"))
    return render_template("index.html", title="ACME Inc. Product Viewer", form=form)

@app.route("/products", methods=["GET", "POST"])
def products():
    return render_template("products.html")