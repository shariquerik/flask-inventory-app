from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from inventory.config import Config


db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)


    from inventory.products.routes import products_bp
    from inventory.locations.routes import locations_bp
    from inventory.movements.routes import movements_bp
    from inventory.dashboard.routes import dashboard_bp

    app.register_blueprint(products_bp)
    app.register_blueprint(locations_bp)
    app.register_blueprint(movements_bp)
    app.register_blueprint(dashboard_bp)

    return app
