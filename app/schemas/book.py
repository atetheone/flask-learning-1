from app import ma
from app.models import Book
from app.schemas.author import AuthorSchema
from app.schemas.category import CategorySchema
from app.schemas.publisher import PublisherSchema

class BookSchema(ma.SQLAlachemySchema):
  class Meta:
    model = Book
  
    book_id = ma.auto_field()
    title = ma.auto_field()
    isbn = ma.auto_field()
    publication_date = ma.auto_field()
    price = ma.auto_field()
    stock = ma.auto_field()
    description = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()
    
    # Only include author and publisher IDs in the basic schema
    _links = ma.Hyperlinks({
			"self": ma.URLFor("books.get_book", values=dict(id="<id>")),
			"author": ma.URLFor("authors.get_author", values=dict(id="<author_id>")),
			"publisher": ma.URLFor("publishers.get_publisher", values=dict(id="<publisher_id>"))
    })

# More detailed schema that includes nested objects
class BookDetailSchema(BookSchema):
	author = ma.Nested(AuthorSchema, exclude=("books", "biography"))
	publisher = ma.Nested(PublisherSchema, exclude=("books", "created_at", "updated_at"))
	categories = ma.Nested(CategorySchema, many=True, exclude=("books", "description", "created_at", "updated_at"))