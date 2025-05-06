from app import db
from datetime import datetime


class Book(db.Model):
  __tablename__ = 'books'
  
  book_id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(200), nullable=False)
  isbn = db.Column(db.String(20), nullable=False, unique=True)
  publication_date = db.Column(db.Date, nullabl=True)
  price = db.Column(db.Numeric(10, 2), nullable=False)
  stock = db.Column(db.Integer, default, 0)
  description = db.Column(db.Text, nullable=True)
  updated_at = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc))
  created_at = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.now(datetime.timezone.utc))
  
  # Foreign keys
  author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'), nullable=False)
  publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.publisher_id'), nullable=False)  
  
  # Relationship
  author = db.relationship('Author', back_populates='books')
  publisher = db.relationship('Publisher', back_populates='books')
  categories = db.relationship('Category', secondary='book_categories', back_populates='books')
  
  def __repr__(self):
    return f'<Book {self.title}'
