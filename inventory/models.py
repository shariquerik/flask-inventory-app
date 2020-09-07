from inventory import db
from datetime import datetime

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(20), unique=True, nullable=False)
    product_description = db.Column(db.String(200), nullable=False, default='This is a default description for product, please update the product with a brief description')
    product_image_file = db.Column(db.String(20), nullable=False, default='default-cars.jpeg')

    def __repr__(self):
        return f"Product('{self.product_name}', '{self.product_image_file}')"


class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(20), unique=True, nullable=False)
    location_description = db.Column(db.String(200), nullable=False, default='This is a default description for location, please update the location with a brief description')
    location_image_file = db.Column(db.String(20), nullable=False, default='thumbnail-default.jpg')

    def __repr__(self):
        return f"Location('{self.location_name}', '{self.location_image_file}')"


class Movement(db.Model):
    movement_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)
    from_location = db.Column(db.String(20), db.ForeignKey('location.location_id'))
    to_location = db.Column(db.String(20), db.ForeignKey('location.location_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Movement( '{self.timestamp}', '{self.from_location}', '{self.to_location}', '{self.product_id}', '{self.qty}')"
