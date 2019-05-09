from product_viewer_app import celery

@celery.task
def save_product_data():
    print("Hello")