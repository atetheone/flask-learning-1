from app import db
from datetime import datetime

class Author(db.Model):
  __tablename__ = 'authors'
  
  author_id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(50), nullable=False)
  last_name = db.Column(db.String(50), nullable=False)
  birth_date = db.Column(db.Date, nullable=True)
  biography = db.Column(db.Text, nullable=True)
  created_at = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc))
  updated_at = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.now(datetime.timezone.utc))
  
  # Relationships
  books = db.relationship('Book', back_populates='author', lazy='dynamic')
  
  def __repr__(self):
    return f'<Author {self.first_name} {self.last_name}'