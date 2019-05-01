from product_viewer_app import app, db
from flask import render_template, flash, redirect, url_for, request

@app.route("/")
@app.route("/index")
def index():
    return "Hello, World"