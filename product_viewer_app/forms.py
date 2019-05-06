from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired

from product_viewer_app import csv

class UploadForm(FlaskForm):
    name = StringField("Name")
    description = TextAreaField("Description")
    file = FileField("CSV File", validators=[FileRequired(), FileAllowed(csv, ".csv files only")])