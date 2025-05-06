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
  
  # Register blueprints
  from app.routes import authors_bp, books_bp, publishers_bp, categories_bp
  app.register_blueprint(authors_bp, url_prefix='/api/authors')
  app.register_blueprint(publishers_bp, url_prefix='/api/publishers')
  app.register_blueprint(categories_bp, url_prefix='/api/categories')
  app.register_blueprint(books_bp, url_prefix='/api/books')
  
  # Shell context processor
  @app.shell_context_processor
  def make_shell_context():
    return dict(app=app, 
                db=db, 
                Author=Author, 
                Book=Book, 
                Publisher=Publisher,
                Category=Category)
  
  return app

# Import models here to avoid circular imports
from app.models import Author, Book, Publisher, Category
  
  