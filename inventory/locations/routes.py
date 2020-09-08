from flask import render_template, url_for, flash, redirect, request, Blueprint
from inventory import db
from inventory.locations.forms import LocationForm, UpdateLocationForm
from inventory.models import Location
from inventory.utils import save_picture

locations_bp = Blueprint('locations_bp', __name__)


# Location


@locations_bp.route('/search_location')
def search_location():
    query = request.args.get('query')
    locations = Location.query.filter(Location.location_name.contains(query)).all()
    return render_template('locations.html', locations=locations, title='Location')

@locations_bp.route('/locations', methods=['GET'])
def locations():
    locations = Location.query.order_by(Location.location_name).all()
    return render_template('locations.html', locations=locations, title='Location')

@locations_bp.route('/locations/new', methods=['GET', 'POST'])
def new_location():
    form = LocationForm()
    if form.validate_on_submit():
        if form.location_picture.data:
            picture_file = save_picture(form.location_picture.data)
        else:
            picture_file = 'thumbnail-default.jpg'
        location = Location(location_name=form.location_name.data, location_description=form.location_description.data, location_image_file=picture_file)
        db.session.add(location)
        db.session.commit()
        flash('Your location is successfully added in the location list!', 'green')
        return redirect(url_for('locations_bp.locations'))
    return render_template('create_location.html', form=form, title='Add New Location')

@locations_bp.route("/location/<int:location_id>")
def location(location_id):
    location = Location.query.get_or_404(location_id)
    return render_template('location.html', title='Update Location', location=location)

@locations_bp.route("/location/<int:location_id>/update", methods=['GET', 'POST'])
def update_location(location_id):
    location = Location.query.get_or_404(location_id)
    form = UpdateLocationForm()

    if not location.location_name == form.location_name.data:
        form = LocationForm()

    if form.validate_on_submit():
        if form.location_picture.data:
            print(form.location_picture.data)
            picture_file = save_picture(form.location_picture.data)
            location.location_image_file = picture_file
        location.location_description = form.location_description.data
        location.location_name = form.location_name.data
        db.session.commit()
        flash('Your location has been updated!', 'green')
        return redirect(url_for('locations_bp.location', location_id=location.location_id))
    elif request.method == 'GET':
        form.location_name.data = location.location_name
        form.location_description.data = location.location_description
    form.submit.label.text = 'Update Location'
    return render_template('create_location.html', title='Update Location', form=form, legend='Update Location') 
