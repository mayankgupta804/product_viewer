from flask import render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import create_engine
from celery.result import AsyncResult

from product_viewer_app import app, db, celery, r
from .helpers import save_file, is_name_unique
from .forms import UploadForm
from .celery_tasks import save_product_data, fetch_paginated_results

import json
import os

@app.route("/", methods=["GET", "POST"])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        if is_name_unique(filename):
            file_id = save_file(form)
            save_product_data.delay(file_id)
            fetch_paginated_results.delay(file_id)
            return render_template("loader.html", file_id=file_id)
        else:
            flash("Please provide a different name.", category="error")    
    return render_template("index.html", title="ACME Inc. Product Viewer", form=form)

@app.route("/products")
def products():
    file_id = request.args.get('file_id', '')
    result = json.loads(r.get(file_id))
    new_result = []
    for item in result:
        res = {}
        for key, val in item.items():
            res[str(key)] = str(val)
        new_result.append(res)
    return render_template("products.html", products=new_result) 

@app.route("/products/fetch")
def fetch_all_products():
    file_id = request.args.get('file_id', '')
    result = r.get(file_id).decode("utf-8")
    if result is "incomplete":
        response = app.response_class(
            response=json.dumps("incomplete"),
            status=200,
            mimetype="application/json"
        )
    else:
        response = app.response_class(
            response=json.dumps(result),
            status=200,
            mimetype="application/json",
        )
    return response

@app.route("/products/<int:index>", methods=["GET", "PUT", "DELETE"])
def operate_on_product(index):
    # if request.method == "GET":
    #     index = request.args.get('index', '')
    #     if index is '':
    #         return redirect(url_for("products"))
    pass

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500