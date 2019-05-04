from product_viewer_app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    sku = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(300))

    def __repr__(self):
        return '<Product {}>'.format(self.sku)   