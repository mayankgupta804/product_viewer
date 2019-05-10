from sqlalchemy import create_engine, orm

from product_viewer_app import app, celery, db
from .models import FileMetaData

import pandas as pd

@celery.task
def save_product_data(id):
    try:
        csv_obj = db.session.query(FileMetaData).filter_by(id=id).first()
    except orm.exc.NoResultFound:
        return 
    path = csv_obj.path
    df = pd.read_csv(path)
    engine = create_engine(app.config.get("SQLALCHEMY_DATABASE_URI"))
    df.to_sql(csv_obj.filename, con=engine)
    connection = engine.connect()
    connection.execute("ALTER TABLE {} ADD COLUMN is_active BOOLEAN DEFAULT '1' NOT NULL".format(csv_obj.filename))

@celery.task
def fetch_paginated_results(page_num):
    pass