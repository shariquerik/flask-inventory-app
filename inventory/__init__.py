from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from inventory.config import Config


app = Flask(__name__)
app.config['SECRET_KEY'] = '4791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['WHOOSH_BASE']='whoosh'
db = SQLAlchemy(app)


from inventory import models
from inventory import routes