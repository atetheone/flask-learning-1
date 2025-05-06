from app import ma
from app.models import Author
from marshmallow import fields

class AuthorSchema(ma.SQLAlchemySchema):
  class Meta:
    models = Author
  
  author_id = ma.auto_field()
  first_name = ma.auto_field()
  last_name = ma.auto_field()
  birth_date = ma.auto_field()
  biography = ma.auto_field()
  created_at = ma.auto_field()
  updated_at = ma.auto_field()
  
  full_name = fields.Method("get_full_name")
  
  def get_full_name(self, obj):
    return f"{obj.first_name} {obj.last_name}"
  
  # Add url for nested resource
  _links = ma.Hyperlinks({
		"self": ma.URLFor("authors.get_author", values=dict(id="<id>")),
		"books": ma.URLFor("athors.get_author_books", values=dict(id="<id>"))
	})