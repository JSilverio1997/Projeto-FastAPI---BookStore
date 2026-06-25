from fastapi.encoders import jsonable_encoder
from rich.console import Console
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from src.utils.utils import write_json


username = "root"
password = ""
database_name = "bookstore_db"
database_url = f"mysql+pymysql://{username}:{password}@localhost:3306/{database_name}"

engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

console = Console()


def init_db() -> None:
    """Create database tables if they do not exist yet."""
    from src.models.book import Book  # noqa: F401

    Base.metadata.create_all(bind=engine)

    from src.crud.book_crud import read_books
    books_list = jsonable_encoder(read_books(next(get_db())))
    print(books_list)
    write_json(books_list)


def get_db():
    database = SessionLocal()
    try:
        console.print(f"Open connection: {database_name}")
        yield database
    finally:
        database.close()
        console.print(f"Close connection: {database_name}")


if __name__ == "__main__":
    try:
        init_db()
        with SessionLocal() as db:
            console.print("Connection is opened")

        console.print("Connection is closed")

    except Exception as e:
        console.print(f"Error: {e}")
