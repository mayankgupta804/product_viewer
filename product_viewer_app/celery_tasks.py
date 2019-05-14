from sqlalchemy import create_engine, orm

from product_viewer_app import app, celery, db
from .models import FileMetaData
from .helpers import get_db_connection, get_file_object

import pandas as pd
import time
import json
import redis

# Configure redis for caching
r = redis.StrictRedis()

@celery.task(bind=True, default_retry_delay=10, max_retries=20, acks_late=True)
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

@celery.task(bind=True, default_retry_delay=10, max_retries=20, acks_late=True)
def fetch_paginated_results(self, file_id, page_num=0, *args, **kwargs):
    r.set(file_id, "incomplete")
    file_obj = get_file_object(file_id)
    connection = get_db_connection()
    page_size = 25
    fetch_products_query = "SELECT * FROM {} LIMIT {} OFFSET {}".format(file_obj.filename, page_size, page_num*page_size)
    try:
        query_result = connection.execute(fetch_products_query)
    except Exception as e:
        self.retry(exc=e)
    result = []  
    for row in query_result:
        result.append(dict(row.items()))
    r.set(file_id, json.dumps(result))    

@celery.task(bind=True, default_retry_delay=10, max_retries=20, acks_late=True)
def delete_all_products(self, file_id):
    # Get details of table that needs to be deleted
    file_obj = get_file_object(file_id)
    
    connection = get_db_connection()
    delete_query = "DROP TABLE {}".format(file_obj.filename)
    try:
        query_result = connection.execute(delete_query)
    except Exception as e:
        self.retry(exc=e)

    # Remove all file metadata    
    db.session.query(FileMetaData).filter_by(id=file_id).delete()
    db.session.commit()    