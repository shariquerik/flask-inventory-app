from flask import render_template, url_for, flash, redirect, request, Blueprint
from inventory import db
from inventory.products.forms import ProductForm, UpdateProductForm
from inventory.models import Product
from inventory.utils import save_picture

products_bp = Blueprint('products_bp', __name__)

# Product

@products_bp.route('/search_product')
def search_product():
    query = request.args.get('query')
    products = Product.query.filter(Product.product_name.contains(query)).all()
    return render_template('products.html', products=products, title='Product')

@products_bp.route('/products', methods=['GET', 'POST'])
def products():
    products = Product.query.order_by(Product.product_name).all()
    return render_template('products.html', products=products, title='Product', label='Add Product')

@products_bp.route('/products/new', methods=['GET', 'POST'])
def new_product():
    form = ProductForm()
    if form.validate_on_submit():
        if form.product_picture.data:
            picture_file = save_picture(form.product_picture.data)
        else:
            picture_file = 'default-cars.jpeg'
        product = Product(product_name=form.product_name.data, product_description=form.product_description.data, product_image_file=picture_file)
        db.session.add(product)
        db.session.commit()
        flash('Your product is successfully added in the product list!', 'green')
        return redirect(url_for('products_bp.products'))
    return render_template('create_product.html', form=form, title='Add New Product')

@products_bp.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', title='Update Product', product=product)

@products_bp.route("/product/<int:product_id>/update", methods=['GET', 'POST'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = UpdateProductForm()

    if not product.product_name == form.product_name.data:
        form = ProductForm()

    if form.validate_on_submit():
        if form.product_picture.data:
            picture_file = save_picture(form.product_picture.data)
            product.product_image_file = picture_file
        product.product_description = form.product_description.data
        product.product_name = form.product_name.data
        db.session.commit()
        flash('Your product has been updated!', 'green')
        return redirect(url_for('products_bp.product', product_id=product.product_id))
    elif request.method == 'GET':
        form.product_name.data = product.product_name
        form.product_description.data = product.product_description
    form.submit.label.text = 'Update Product'
    return render_template('create_product.html', title='Update Product', form=form, legend='Update Product')

