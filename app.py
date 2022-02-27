from flask import Flask
from flask_cors import CORS
from src.database import db, migrate
from src.views.base import base
from src.views.api import api
from os import environ

app = Flask(__name__)
CORS(app, resources={r'/api/*': {'origin': '*'}})

ENV = environ.get('FLASK_ENV')

if ENV == 'development':
    app.debug = True
    DATABASE_URL = 'sqlite:///test.db'

elif ENV == 'production':
    app.debug = False
    DATABASE_URL = environ.get('MY_DATABASE_URL')

else:
    raise Exception('FLASK_ENV not found / not supported')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(base)
app.register_blueprint(api, url_prefix='/api')