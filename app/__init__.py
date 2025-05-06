from flask import Flask
from flask_sqlachemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import config

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_name='default'):
  app = Flask(__name__)
  app.config.from_object(config[config_name])
  
  # Initialize extensions with app
  db.init_app(app)
  ma.init_app(app)