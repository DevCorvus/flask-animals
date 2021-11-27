from flask import Flask
from flask_cors import CORS
from src.database import db, migrate
from src.views.base import base
from src.views.api import api
from os import environ

app = Flask(__name__)
CORS(app, resources={r'/api/*': {'origin': '*'}})

ENV = 'development'

if ENV == 'development':
    app.debug = True
    DATABASE_URL = 'sqlite:///test.db'

elif ENV == 'production':
    app.debug = False
    DATABASE_URL = environ['MY_DATABASE_URL']

else:
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(base)
app.register_blueprint(api, url_prefix='/api')