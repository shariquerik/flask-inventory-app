from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from inventory.models import Product, Location

class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    product_description = TextAreaField('Description')
    product_picture = FileField('Update Product Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'jfif'])])
    submit = SubmitField('Add Product')

    def validate_product_name(self, product_name):
        product = Product.query.filter_by(product_name=product_name.data).first()
        if product:
            raise ValidationError('That product is available. Please choose a different one.')

class UpdateProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    product_description = TextAreaField('Description')
    product_picture = FileField('Update Product Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'jfif'])])
    submit = SubmitField('Add Product')


class LocationForm(FlaskForm):
    location_name = StringField('Location Name', validators=[DataRequired()])
    location_description = TextAreaField('Description')
    location_picture = FileField('Update Location Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'jfif'])])
    submit = SubmitField('Add Location')

    def validate_location_name(self, location_name):
        location = Location.query.filter_by(location_name=location_name.data).first()
        if location:
            raise ValidationError('That location is available. Please choose a different one.')

class UpdateLocationForm(FlaskForm):
    location_name = StringField('Location Name', validators=[DataRequired()])
    location_description = TextAreaField('Description')
    location_picture = FileField('Update Location Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'jfif'])])
    submit = SubmitField('Add Location')


class MovementForm(FlaskForm):
    from_location = SelectField(u'From', coerce=int)
    to_location = SelectField(u'To', coerce=int)
    product_id = SelectField('Product Name', coerce=int, validators=[DataRequired()])
    qty = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Move Product')