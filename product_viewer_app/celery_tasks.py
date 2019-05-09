from product_viewer_app import celery, db
from .models import FileMetaData

@celery.task
def save_product_data(id):
    csv_obj = db.session.query(FileMetaData).filter_by(id=id).first()
    path = csv_obj.path
    print(path)