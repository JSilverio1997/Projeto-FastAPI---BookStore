from sqlalchemy import exists
from sqlalchemy.orm import Session
from src.models.book import Book
from src.schemas.book import BookDb


def check_book_record(book_id: str, db: Session) -> int | None:
    check_book = db.query(exists().where(Book.book_id == book_id)).scalar()
    return check_book


def return_obj_book_orm(book_id: str, db: Session) -> Book | None:
    return db.query(Book).filter(Book.book_id == book_id).first()


def read_books(db: Session) -> list:
    books = [BookDb.model_validate(book, from_attributes=True) for book in db.query(Book).all()]
    return books


def create_book(new_book: dict, db: Session) -> bool:
    new_book_model = Book(**new_book)

    created_book = check_book_record(new_book_model.book_id, db)
    if created_book is False:
        db.add(new_book_model)
        db.commit()
        db.refresh(new_book_model)
        exist_book = check_book_record(new_book_model.book_id, db)

        if exist_book:
            created_book = True

    return created_book


def delete_book(book_id: str, db: Session) -> bool:
    book = return_obj_book_orm(book_id, db)
    if book:
        db.delete(book)
        db.commit()
        book_id_deleted = check_book_record(book_id, db)
        if not book_id_deleted:
            return True

    return False


def update_book_crud(book_id: str, book: dict, db: Session) -> Book | None:
    book_update_model = Book(**book)
    check_book_id = check_book_record(book_id, db)
    if check_book_id:
        book_db = return_obj_book_orm(book_id, db)

        if book_update_model.book_name is not None:
            book_db.book_name = book_update_model.book_name

        if book_update_model.genre is not None:
            book_db.genre = book_update_model.genre

        if book_update_model.price is not None:
            book_db.price = book_update_model.price

        db.commit()
        db.refresh(book_db)

        return book_db

    return None
