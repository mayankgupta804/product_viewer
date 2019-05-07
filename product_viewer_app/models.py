from product_viewer_app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    sku = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(300))

    def __repr__(self):
        return '<Product {}>'.format(self.name)   

class FileMetaData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64))
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(300))
    path = db.Column(db.String(100))

    def __repr__(self):
        return '<Filename {}>'.format(self.name)  