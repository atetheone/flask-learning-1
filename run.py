from app import create_app, db
from app.models import Author, Book, Category, Publisher
import click
import os

# Create the Flask application instance using the factory function
app = create_app(os.getenv("FLASK_ENV", "development"))


# Add a basic route to confirm the app is running
@app.route("/")
def index():
    return {
        "message": "Welcome to the Bookstore API",
        "version": "1.0",
        "endpoints": {
            "authors": "/api/authors",
            "books": "/api/books",
            "categories": "/api/categories",
            "publishers": "/api/publishers",
        },
    }


# Create a shell context that adds database and model objects to the shell sess
@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Author": Author,
        "Book": Book,
        "Category": Category,
        "Publisher": Publisher,
    }


@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Database initialized!")


@app.cli.command("drop-db")
@click.confirmation_option(prompt="Are you sure you want to drop all tables?")
def drop_db():
    """Drop all database tables."""
    db.drop_all()
    click.echo("Database tables dropped successfully.")


@app.cli.command("seed-db")
def seed_db():
    """Seed the database with sample data."""
    # Create sample authors
    authors = [
        Author(
            first_name="Jane",
            last_name="Austen",
            biography="English novelist known for her six major novels.",
        ),
        Author(
            first_name="George",
            last_name="Orwell",
            biography="English novelist and essayist.",
        ),
        Author(
            first_name="J.K.",
            last_name="Rowling",
            biography="British author, philanthropist, and film producer.",
        ),
    ]

    # Create sample publishers
    publishers = [
        Publisher(name="Penguin Books", website="https://www.penguin.com"),
        Publisher(name="Bloomsbury", website="https://www.bloomsbury.com"),
        Publisher(
            name="Vintage Books",
            website="https://www.penguinrandomhouse.com/brands/vintage/",
        ),
    ]

    # Create sample categories
    categories = [
        Category(name="Fiction", description="Invented stories and narration"),
        Category(name="Classics", description="Works of enduring excellence"),
        Category(
            name="Fantasy",
            description="Books featuring magical and supernatural elements",
        ),
        Category(
            name="Dystopian",
            description=(
                "Books set in an imagined society characterized by " "suffering"
            ),
        ),
    ]

    # Add to session
    db.session.add_all(authors)
    db.session.add_all(publishers)
    db.session.add_all(categories)
    db.session.commit()

    # Create books with relationships
    books = [
        Book(
            title="Pride and Prejudice",
            isbn="9780141439518",
            price=9.99,
            stock=25,
            description="A romantic novel of manners.",
            author_id=1,  # Jane Austen
            publisher_id=1,  # Penguin Books
        ),
        Book(
            title="1984",
            isbn="9780451524935",
            price=12.99,
            stock=15,
            description="A dystopian social science fiction novel.",
            author_id=2,  # George Orwell
            publisher_id=3,  # Vintage Books
        ),
        Book(
            title="Harry Potter and the Philosopher's Stone",
            isbn="9780747532743",
            price=14.99,
            stock=50,
            description="The first novel in the Harry Potter series.",
            author_id=3,  # J.K. Rowling
            publisher_id=2,  # Bloomsbury
        ),
    ]

    db.session.add_all(books)
    db.session.commit()

    # Add categories to books
    books[0].categories.extend([categories[0], categories[1]])
    books[1].categories.extend(
        [categories[0], categories[1], categories[3]]
    )  # Fiction, Classics, Dystopian
    books[2].categories.extend([categories[0], categories[2]])

    db.session.commit()

    click.echo("Database seeded successfully with sample data!")


@app.cli.command("reset-db")
@click.confirmation_option(prompt="Are you sure you want to reset the database?")
def reset_db():
    """Drop all tables, recreate them, and seed with sample data."""
    db.drop_all()
    click.echo("Database tables dropped.")
    db.create_all()
    click.echo("Database tables created.")

    # Call the seed function directly
    ctx = app.cli.get_command("seed-db").callback
    ctx()


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
