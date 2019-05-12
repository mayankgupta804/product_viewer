from sqlalchemy import create_engine, orm

from product_viewer_app import app, celery, db
from .models import FileMetaData
from .helpers import get_db_connection, get_file_object

import pandas as pd
import time
import json
import redis

# Configure redis for caching
r = redis.Redis(host="localhost", port=6379, db=0)

@celery.task(bind=True, default_retry_delay=30, max_retries=60, acks_late=True)
def save_product_data(self, file_id, *args, **kwargs):
    try:
        csv_obj = db.session.query(FileMetaData).filter_by(id=file_id).first()
    except orm.exc.NoResultFound as e:
        self.retry(exc=e) 
    path = csv_obj.path
    df = pd.read_csv(path)
    engine = create_engine(app.config.get("SQLALCHEMY_DATABASE_URI"))
    df.to_sql(csv_obj.filename, con=engine)
    connection = engine.connect()
    try:
        connection.execute("ALTER TABLE {} ADD COLUMN is_active BOOLEAN DEFAULT '1' NOT NULL".format(csv_obj.filename))
    except orm.exc.NoResultFound as e:
        self.retry(exc=e)        

@celery.task(bind=True, default_retry_delay=30, max_retries=60, acks_late=True)
def fetch_paginated_results(self, file_id, *args, **kwargs):
    file_obj = get_file_object(file_id)
    connection = get_db_connection()
    fetch_products_query = "SELECT * FROM {} LIMIT {}".format(file_obj.filename, 10)
    try:
        result = connection.execute(fetch_products_query)
    except Exception as e:
        self.retry(exc=e)
    r.set(file_id, json.dumps([(dict(row.items())) for row in result]))
    