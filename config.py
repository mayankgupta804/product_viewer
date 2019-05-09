import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'easy-peasy'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'product_viewer_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TOP_LEVEL_DIR="/Users/mayank/Documents/Flask Projects/product_viewer"

    # Uploads
    UPLOADS_DEFAULT_DEST = TOP_LEVEL_DIR + '/static/csv/'
    UPLOADS_DEFAULT_URL = 'http://127.0.0.1:5000/static/csv/'
    
    UPLOADED_CSV_DEST = TOP_LEVEL_DIR + '/static/csv/'
    UPLOADED_CSV_URL = 'http://127.0.0.1:5000/static/csv/'

    MAX_CONTENT_LENGTH = 100 * 1024 * 1024

    CELERY_RESULTS_BACKEND = os.environ.get("REDIS_URL") or "redis://localhost:6379"
    CELERY_BROKER_URL = os.environ.get("CLOUDAMQP_URL") or "amqp://localhost"
