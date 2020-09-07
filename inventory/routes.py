from flask import render_template, url_for, flash, redirect, request
from inventory import app, db
from inventory.forms import ProductForm, LocationForm, MovementForm
from inventory.models import Product, Location, Movement
from datetime import datetime

# Home
@app.route('/home')
def home():
    return render_template('home.html')

# Dashboard
@app.route('/')
@app.route("/dashboard")
def dashboard():
    movements = db.session.query(Movement.to_location, Movement.product_id).filter(Movement.from_location=="").distinct(Movement.to_location).all()
    product = Product.query
    qty = Movement.query
    return render_template('dashboard.html', title='Dashboard', movements=movements, qty=qty, product=product)


# Search
@app.route('/search_product')
def search_product():
    query = request.args.get('query')
    products = Product.query.filter(Product.product_name.contains(query)).all()
    return render_template('products.html', products=products, title='Product')

@app.route('/search_location')
def search_location():
    query = request.args.get('query')
    locations = Location.query.filter(Location.location_name.contains(query)).all()
    return render_template('locations.html', locations=locations, title='Location')

@app.route('/search_movement')
def search_movement():
    query = request.args.get('query')
    product = Product.query.filter(Product.product_name.contains(query)).all()
    from_location = []
    to_location = []
    movements = []
    movements = Movement.query.filter(Movement.from_location.contains(query)).all()
    movements = movements + Movement.query.filter(Movement.to_location.contains(query)).all()
    if product:
        for p in product:
            movements = movements + Movement.query.filter(Movement.product_id==p.product_id).all()
    products = Product.query
    locations = Location.query
    movements = list(dict.fromkeys(movements))
    return render_template('movements.html', movements=movements, title='Movement', products=products, locations=locations)

@app.route('/search_dashboard')
def search_dashboard():
    q = request.args.get('query')
    movements = []
    product = Product.query.filter(Product.product_name.contains(q)).all()
    lists = db.session.query(Movement.to_location, Movement.product_id).filter(Movement.from_location=="").distinct(Movement.to_location).all()
    for i in lists:
        if q.lower() in i[0].lower():
            movements.append(i)
    if product:
        for p in product:
            for i in lists:
                if(p.product_id == i[1]):
                    movements.append(i)
    product = Product.query
    qty = Movement.query
    movements = list(dict.fromkeys(movements))
    return render_template('dashboard.html', title='Dashboard', movements=movements, qty=qty, product=product)


# Product
@app.route('/products', methods=['GET', 'POST'])
def products():
    products = Product.query.order_by(Product.product_name).all()
    return render_template('products.html', products=products, title='Product')

@app.route('/products/new', methods=['GET', 'POST'])
def new_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(product_name=form.product_name.data)
        db.session.add(product)
        db.session.commit()
        flash('Your product is successfully added in the product list!', 'green')
        return redirect(url_for('products'))
    return render_template('create_product.html', form=form, title='New Product')

@app.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', title='Update Product', product=product)

@app.route("/product/<int:product_id>/update", methods=['GET', 'POST'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm()
    if form.validate_on_submit():
        product.product_name = form.product_name.data
        db.session.commit()
        flash('Your product has been updated!', 'green')
        return redirect(url_for('product', product_id=product.product_id))
    elif request.method == 'GET':
        form.product_name.data = product.product_name
    form.submit.label.text = 'Update Product'
    return render_template('create_product.html', title='Update Product', form=form, legend='Update Product') 

@app.route("/product/<int:product_id>/delete", methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Your product has been deleted!', 'green')
    return redirect(url_for('products'))


# Location
@app.route('/locations', methods=['GET'])
def locations():
    locations = Location.query.order_by(Location.location_name).all()
    return render_template('locations.html', locations=locations, title='Location')

@app.route('/locations/new', methods=['GET', 'POST'])
def new_location():
    form = LocationForm()
    if form.validate_on_submit():
        location = Location(location_name=form.location_name.data)
        db.session.add(location)
        db.session.commit()
        flash('Your location is successfully added in the location list!', 'green')
        return redirect(url_for('locations'))
    return render_template('create_location.html', form=form, title='New Location')

@app.route("/location/<int:location_id>")
def location(location_id):
    location = Location.query.get_or_404(location_id)
    return render_template('location.html', title='Update Location', location=location)

@app.route("/location/<int:location_id>/update", methods=['GET', 'POST'])
def update_location(location_id):
    location = Location.query.get_or_404(location_id)
    form = LocationForm()
    if form.validate_on_submit():
        location.location_name = form.location_name.data
        db.session.commit()
        flash('Your location has been updated!', 'green')
        return redirect(url_for('location', location_id=location.location_id))
    elif request.method == 'GET':
        form.location_name.data = location.location_name
    form.submit.label.text = 'Update Location'
    return render_template('create_location.html', title='Update Location', form=form, legend='Update Location') 

@app.route("/location/<int:location_id>/delete", methods=['POST'])
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    flash('Your location has been deleted!', 'green')
    return redirect(url_for('locations'))


# Movement
movements_data = []

def get_choices(form):
    location_choices = [(0, "---")]+[(location.location_id, location.location_name) for location in Location.query.all()]
    form.from_location.choices = location_choices
    form.to_location.choices = location_choices
    form.product_id.choices = [(product.product_id, product.product_name) for product in Product.query.all()]

def convert_location_id_to_name(id):
    if id: return Location.query.filter_by(location_id=id).first().location_name
    elif not id or id == 0: return ""

def convert_location_name_to_id(name):
    if name: return Location.query.filter_by(location_name=name).first().location_id
    else: return 0

def movement_exist(product_id, from_location, to_location):
    return Movement.query.filter_by(from_location=from_location, to_location=to_location, product_id=product_id).first()

def error_conditions(from_location, to_location, qty, existing_prd_in_from_location, existing_prd_in_to_location, check, update_qty):
    #Do not allow to create movement without location in either location field
    if from_location == "" and to_location == "":
        flash('Atleast one location is need', 'red')
    
    #to_location and from_location cannot be same
    elif from_location == to_location:
        flash('Cannot transfer in same location, please select different location', 'red')

    #check if from_location has enough quantity
    elif check == 'new' and existing_prd_in_from_location and ((existing_prd_in_from_location.qty - qty) < 0):
        flash('The quantity of product available in '+ from_location+' is '+ str(existing_prd_in_from_location.qty) + ' which is less than you need', 'red')
    
    #check if from_location exist or not
    elif check == 'new' and not existing_prd_in_from_location and from_location != '':
        flash('The product is not available in '+ from_location + ' location', 'red')
    
    #check if from_location has enough quantity
    elif check == 'update' and existing_prd_in_from_location and ((existing_prd_in_from_location.qty - qty + update_qty) < 0):
        flash('The quantity of product is not available in '+ from_location, 'red')

    #In from location product is not available so throw an error.
    elif (existing_prd_in_to_location and (from_location != "" and to_location != "" and not existing_prd_in_to_location) or to_location == "") and not existing_prd_in_from_location:
        flash('The product is not available in '+ from_location +' location', 'red')

    #Storage Capacity Error
    elif qty > 100 or (existing_prd_in_to_location and existing_prd_in_to_location.qty + qty > 100):
        flash('The quantity of product exceeds the storage capacity(100) of '+to_location+' location. You can only move '+str(100-existing_prd_in_to_location.qty) + ' products.', 'red')

    else:
        return 'No error'

@app.route("/movements/new", methods=['GET', 'POST'])
def new_movement():
    form = MovementForm()

    # Auto fill Product, Location fields on the form
    get_choices(form)

    # Declaring variables
    from_location = convert_location_id_to_name(form.from_location.data)
    to_location = convert_location_id_to_name(form.to_location.data)
    product_id = form.product_id.data
    qty = form.qty.data

    # Check if data already exist
    existing_movement = movement_exist(product_id, from_location, to_location)
    existing_prd_in_from_location = movement_exist(product_id, "", from_location)
    existing_prd_in_to_location = movement_exist(product_id, "", to_location)

    if form.validate_on_submit():
        error = error_conditions(from_location, to_location, qty, existing_prd_in_from_location, existing_prd_in_to_location, 'new', '')
        if(error != 'No error'):
            return redirect(url_for('new_movement'))
        else:
            #qty++ in to_location
            if existing_movement and existing_movement.from_location == "" and existing_movement.to_location != "":
                existing_prd_in_to_location.qty = existing_prd_in_to_location.qty + qty

            #qty-- in from_location
            elif existing_movement and existing_movement.from_location != "" and existing_movement.to_location == "":
                existing_prd_in_from_location.qty = existing_prd_in_from_location.qty - qty

            #qty++ in to_location and qty-- in from_location
            elif (existing_movement and existing_movement.from_location != "" and existing_movement.to_location != "" ) or (existing_prd_in_to_location and existing_prd_in_from_location):
                existing_prd_in_to_location.qty = existing_prd_in_to_location.qty + qty
                existing_prd_in_from_location.qty = existing_prd_in_from_location.qty - qty

            #decrement from from_location and then create to_location
            elif existing_prd_in_from_location and not existing_prd_in_to_location:
                existing_prd_in_from_location.qty = existing_prd_in_from_location.qty - qty
                if to_location != "":
                    product_to = Movement(from_location="", to_location=to_location, product_id=product_id, qty=qty)
                    db.session.add(product_to)
                    db.session.commit()

            #Do Nothing
            else:
                pass
        # 
        movement = Movement(from_location=from_location, to_location=to_location, product_id=product_id, qty=qty)
        db.session.add(movement)
        db.session.commit()
        global movements_data 
        movements_data.insert(0, movement)
        print(movements_data)
        flash('Your product movement is successfully added in the product movement list!', 'green')
        return redirect(url_for('movements'))
    return render_template('create_movement.html', form=form, legend='New Product Movement')

@app.route("/movement/<int:movement_id>")
@app.route("/movement/<int:movement_id>/<int:qty>")
def movement(movement_id, qty=None):
    movement = Movement.query.get_or_404(movement_id)
    products = Product.query
    return render_template('movement.html', title='Update Moved Product', movement=movement, products=products, qty=qty)

@app.route("/movement/<int:movement_id>/update", methods=['GET', 'POST'])
def update_movement(movement_id):
    movement = Movement.query.get_or_404(movement_id)
    form = MovementForm()
    
    # Auto fill Product, Location fields on the form
    get_choices(form)

    # Declaring variables
    from_location = convert_location_id_to_name(form.from_location.data)
    to_location = convert_location_id_to_name(form.to_location.data)
    product_id = form.product_id.data
    qty = form.qty.data

    # Check if data already exist
    existing_movement = movement_exist(product_id, from_location, to_location)
    existing_prd_in_from_location = movement_exist(product_id, "", from_location)
    existing_prd_in_to_location = movement_exist(product_id, "", to_location)

    if form.validate_on_submit(): 
        error = error_conditions(from_location, to_location, qty, existing_prd_in_from_location, existing_prd_in_to_location, "update", movement.qty)
        if(error == 'No error'):
            #qty++ in to_location
            if existing_movement and existing_movement.from_location == "" and existing_movement.to_location != "":
                existing_prd_in_to_location.qty = existing_prd_in_to_location.qty + qty - movement.qty

            #qty-- in from_location
            elif existing_movement and existing_movement.from_location != "" and existing_movement.to_location == "":
                existing_prd_in_from_location.qty = existing_prd_in_from_location.qty - qty + movement.qty

            #qty++ in to_location and qty-- in from_location
            elif (existing_movement and existing_movement.from_location != "" and existing_movement.to_location != "") or (existing_prd_in_to_location and existing_prd_in_from_location):
                existing_prd_in_to_location.qty = existing_prd_in_to_location.qty + qty - movement.qty
                existing_prd_in_from_location.qty = existing_prd_in_from_location.qty - qty + movement.qty

            #decrement from from_location and then create to location
            elif existing_prd_in_from_location and not existing_prd_in_to_location:
                existing_prd_in_from_location.qty = existing_prd_in_from_location.qty - qty + movement.qty
                if to_location != "":
                    product_to = Movement(from_location="", to_location=to_location, product_id=product_id, qty=qty)
                    db.session.add(product_to)
                    db.session.commit()

            #Do Nothing
            else:
                pass
            
            movement.from_location = from_location
            movement.to_location = to_location
            movement.product_id = product_id
            movement.qty = qty
            movement.timestamp = datetime.now()
            db.session.commit()

            index_list = []
            global movements_data
            for i in movements_data:
                index_list.append(i.movement_id)
            index = index_list.index(movement.movement_id)
            tmp = movements_data[index]
            movements_data.remove(tmp)
            movements_data.insert(index, movement)

            flash('Your product movement has been updated!', 'green')
            return redirect(url_for('movement', movement_id=movement.movement_id))
    elif request.method == 'GET':
        print(movement)
        form.from_location.data = convert_location_name_to_id(movement.from_location)
        form.to_location.data = convert_location_name_to_id(movement.to_location)
        form.product_id.data = movement.product_id
        form.qty.data = movement.qty
    form.submit.label.text = 'Update Product Movement'
    return render_template('create_movement.html', title='Update Moved Product', form=form, legend='Update Moved Product') 

@app.route("/movement/<int:movement_id>/delete", methods=['POST'])
def delete_movement(movement_id):
    pass

@app.route("/movements")
def movements():
    products = Product.query
    locations = Location.query
    return render_template('movements.html', title='Movement',movements=movements_data, products=products, locations=locations)