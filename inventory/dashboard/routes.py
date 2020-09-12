from flask import render_template, redirect,url_for, request, Blueprint
from inventory import db
from inventory.models import Product, Movement


dashboard_bp = Blueprint('dashboard_bp', __name__)

# Dashboard
@dashboard_bp.route('/')
@dashboard_bp.route("/dashboard")
def dashboard():
    movements = db.session.query(Movement.to_location, Movement.product_id).filter(Movement.from_location=="").distinct(Movement.to_location).all()
    product = Product.query
    qty = Movement.query
    return render_template('dashboard.html', title='Dashboard', movements=movements, qty=qty, product=product)

@dashboard_bp.route('/search_dashboard')
def search_dashboard():
    
    q = request.args.get('query')
    movements = []
    if not q:
        return dashboard()
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
    return render_template('dashboard.html', title='Dashboard', movements=movements, qty=qty, product=product, label='Search Dashboard')