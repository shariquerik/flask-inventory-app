from flask import render_template, url_for, flash, redirect, request, Blueprint
from inventory import db
from inventory.movements.forms import MovementForm
from inventory.models import Product, Location, Movement, StaticMovement
from datetime import datetime
from pytz import timezone

movements_bp = Blueprint('movements_bp', __name__)

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
    elif qty > 100 or (existing_prd_in_to_location and existing_prd_in_to_location.qty + qty - update_qty > 100):
        flash('The quantity of product exceeds the storage capacity(100) of '+to_location+' location. You can only move '+str(100-existing_prd_in_to_location.qty) + ' products.', 'red')

    else:
        return 'No error'

def date_convertion():
    now_utc = datetime.now(timezone('UTC'))
    now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
    return now_asia


@movements_bp.route('/search_movement')
def search_movement():
    query = request.args.get('query')
    product = Product.query.filter(Product.product_name.contains(query)).all()
    from_location = []
    to_location = []
    movements = []
    movements = StaticMovement.query.filter(StaticMovement.from_location.contains(query)).all()
    movements = movements + StaticMovement.query.filter(StaticMovement.to_location.contains(query)).all()
    if product:
        for p in product:
            movements = movements + StaticMovement.query.filter(StaticMovement.product_id==p.product_id).all()
    products = Product.query
    locations = Location.query
    movements = list(dict.fromkeys(movements))
    return render_template('movements.html', movements=movements, title='Search Result', products=products, locations=locations, label='Movement')

@movements_bp.route("/movements")
def movements():
    movements = StaticMovement.query.order_by(StaticMovement.timestamp.desc()).all()
    products = Product.query
    locations = Location.query
    return render_template('movements.html', title='Movement',movements=movements, products=products, locations=locations, label="Move Item")

@movements_bp.route("/movements/new", methods=['GET', 'POST'])
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
        error = error_conditions(from_location, to_location, qty, existing_prd_in_from_location, existing_prd_in_to_location, 'new', 0)
        if(error != 'No error'):
            return redirect(url_for('movements_bp.new_movement'))
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
                    product_to = Movement(from_location="", to_location=to_location, product_id=product_id, qty=qty,timestamp=date_convertion())
                    db.session.add(product_to)
                    db.session.commit()

            else:
                movement = Movement(from_location=from_location, to_location=to_location, product_id=product_id, qty=qty,timestamp=date_convertion())
                db.session.add(movement)

        if from_location != "" and to_location != "":
            movement = Movement(from_location=from_location, to_location=to_location, product_id=product_id, qty=qty,timestamp=date_convertion())
            db.session.add(movement)

        static_movement = StaticMovement(from_location=from_location, to_location=to_location, product_id=product_id, qty=qty,timestamp=date_convertion())
        db.session.add(static_movement)
        db.session.commit()
        
        flash('Your product movement is successfully added in the product movement list!', 'green')
        return redirect(url_for('movements_bp.movements'))
    return render_template('create_movement.html', form=form, legend='New Product Movement', title='Move Product', label='Movement')

@movements_bp.route("/movement/<int:movement_id>")
@movements_bp.route("/movement/<int:movement_id>/<int:qty>")
def movement(movement_id, qty=None):
    movement = StaticMovement.query.get_or_404(movement_id)
    products = Product.query
    return render_template('movement.html', title='Update Moved Product', movement=movement, products=products, qty=qty, label='Movement')

@movements_bp.route("/movement/<int:movement_id>/update", methods=['GET', 'POST'])
def update_movement(movement_id):
    
    static_movement = StaticMovement.query.get_or_404(movement_id)
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
        error = error_conditions(from_location, to_location, qty, existing_prd_in_from_location, existing_prd_in_to_location, "update", static_movement.qty)
        if(error == 'No error'):
            #qty++ in to_location
            if existing_movement and existing_movement.from_location == "" and existing_movement.to_location != "":
                print(existing_prd_in_to_location.qty)
                print(qty)
                print(static_movement.qty)
                existing_prd_in_to_location.qty = existing_prd_in_to_location.qty + qty - static_movement.qty
                print(existing_prd_in_to_location.qty)

            #qty-- in from_location
            elif existing_movement and existing_movement.from_location != "" and existing_movement.to_location == "":
                existing_prd_in_from_location.qty = existing_prd_in_from_location.qty - qty + static_movement.qty

            #qty++ in to_location and qty-- in from_location
            elif (existing_movement and existing_movement.from_location != "" and existing_movement.to_location != "") or (existing_prd_in_to_location and existing_prd_in_from_location):
                existing_prd_in_to_location.qty = existing_prd_in_to_location.qty + qty - static_movement.qty
                existing_prd_in_from_location.qty = existing_prd_in_from_location.qty - qty + static_movement.qty

            #decrement from from_location and then create to location
            elif existing_prd_in_from_location and not existing_prd_in_to_location:
                existing_prd_in_from_location.qty = existing_prd_in_from_location.qty - qty + static_movement.qty
                if to_location != "":
                    product_to = Movement(from_location="", to_location=to_location, product_id=product_id, qty=qty)
                    db.session.add(product_to)
                    db.session.commit()

            #Do Nothing
            else:
                pass


            if to_location != '' and from_location != '':
                existing_movement.from_location = from_location
                existing_movement.to_location = to_location
                existing_movement.product_id = product_id
                existing_movement.qty = qty
                existing_movement.timestamp = date_convertion()
            

            static_movement.from_location = from_location
            static_movement.to_location = to_location
            static_movement.product_id = product_id
            static_movement.qty = qty
            static_movement.timestamp = date_convertion()

            db.session.commit()

            flash('Your product movement has been updated!', 'green')
            return redirect(url_for('movements_bp.movement', movement_id=static_movement.movement_id))
    elif request.method == 'GET':
        form.from_location.data = convert_location_name_to_id(static_movement.from_location)
        form.to_location.data = convert_location_name_to_id(static_movement.to_location)
        form.product_id.data = static_movement.product_id
        form.qty.data = static_movement.qty
    form.submit.label.text = 'Update Product Movement'
    return render_template('create_movement.html', title='Update Moved Product', form=form, label='Movement')