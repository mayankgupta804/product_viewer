from product_viewer_app import db

class FileMetaData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64), index=True, unique=True)
    path = db.Column(db.String(100))

    def __repr__(self):
        return '<Filename {}>'.format(self.filename)  