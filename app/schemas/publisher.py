from app import ma
from app.models import Publisher

class PublisherSchema(ma.SQLAlachemySchema):
  class Meta:
    model = Publisher
  
    publisher_id = ma.auto_field()
    name = ma.auto_field()
    address = ma.auto_field()
    website = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()
    
    _links = ma.Hyperlinks({
			"self": ma.URLFor("publishers.get_publisher", values=dict(id="<id>")),
			"books": ma.URLFor("publishers.get_publisher_books", values=dict(id="<id>"))
    })