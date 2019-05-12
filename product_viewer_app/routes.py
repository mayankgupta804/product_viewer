from flask import render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import create_engine

from product_viewer_app import app, db
from .helpers import save_file, is_name_unique
from .forms import UploadForm
from .celery_tasks import save_product_data, fetch_paginated_results

import os

@app.route("/", methods=["GET", "POST"])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        if is_name_unique(filename):
            file_id = save_file(form)
            save_product_data.delay(file_id)
            return redirect(url_for("products", file_id=file_id))
        else:
            flash("Please provide a different name.", category="error")    
    return render_template("index.html", title="ACME Inc. Product Viewer", form=form)

@app.route("/products")
def products():
    file_id = int(request.args.get('file_id', ''))
    fetch_paginated_results.delay(file_id)
    return render_template("products.html")

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500