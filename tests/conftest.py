import pytest
from app import create_app, db
from app.models import Author, Book, Category, Publisher
# from datetime import date


@pytest.fixture
def app():
    """Create application for the tests."""
    app = create_app('testing')

    # Create tables and context
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()


@pytest.fixture
def sample_data(app):
    """Create sample data for testing."""
    with app.app_context():
        # Create authors
        author1 = Author(first_name="John", last_name="Doe")
        author2 = Author(first_name="Jane", last_name="Does")
        db.session.add_all([author1, author2])

        # Create publishers
        publisher1 = Publisher(name="Test Publisher")
        publisher2 = Publisher(name="Another Press")
        db.session.add_all([publisher1, publisher2])

        # Create categories
        fiction = Category(name="Fiction")
        nonfiction = Category(name="Non-Fiction")
        scifi = Category(name="Science Fiction")
        db.session.add_all([fiction, nonfiction, scifi])

        db.session.commit()

        # Create books
        book1 = Book(
            title="Test Book",
            isbn="1234567890123",
            price=9.99,
            stock=10,
            author_id=author1.author_id,
            publisher_id=publisher1.publisher_id,
            description="A test book"
        )

        db.session.add(book1)
        db.session.flush()  # Flush to ensure book1 has an ID
        book1.categories.append(fiction)

        book2 = Book(
            title="Another Book",
            isbn="9876543210987",
            price=19.99,
            stock=5,
            author_id=author2.author_id,
            publisher_id=publisher2.publisher_id,
            description="Another test book"
        )

        db.session.add(book2)
        db.session.flush()  # Flush to ensure book2 has an ID

        # Now safe to establish relationships
        book2.categories.extend([fiction, scifi])

        # Commit all changes
        db.session.commit()

        # Return the IDs for use in tests
        return {
            'authors': [author1.author_id, author2.author_id],
            'publishers': [publisher1.publisher_id, publisher2.publisher_id],
            'categories': [
                [fiction.category_id, fiction.name],
                [nonfiction.category_id, nonfiction.name],
                [scifi.category_id, scifi.name]
            ],
            'category_ids': [
                fiction.category_id,
                scifi.category_id
            ],
            'books': [book1.book_id, book2.book_id]
        }
