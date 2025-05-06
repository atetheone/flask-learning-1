from app import db
from datetime import datetime

# Assoc table many-to-many books and categories
book_categories = db.Table('book_categories', 
  db.Column('book_id', db.Integer, db.ForeignKey('books.book_id'), primary_key=True),
  db.Column('category_id', db.Integer, db.ForeignKey('categories.category_id'), primary_key=True),
)

# Main table class
class Category(db.Model):
  __tablename__ = 'categories'
  
  category_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False, unique=True)
  description = db.Column(db.Text, nullable=True)
  updated_at = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc))
  created_at = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.now(datetime.timezone.utc))
  
  # Relationship
  books = db.relationship('Book', secondary=book_categories, back_populates='categories')
  
  def __repr__(self):
    return f'<Category {self.name}'
