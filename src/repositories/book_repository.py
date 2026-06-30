from fastapi.encoders import jsonable_encoder
from src.utils.utils import read_json, write_json, read_csv, write_csv, write_log
from typing import Any, Optional
from src.crud.book_crud import create_book, delete_book, update_book_crud
from sqlalchemy.orm import Session
from src.schemas.book import BookCreateOut
from src.exception.book_exception_csv import BookExceptionCsv, ValidationRulesBookCsv


def load_book_database() -> list[dict]:
    return read_json()


def get_all_books() -> list[dict]:
    return load_book_database()


def get_book_by_index(index: int) -> Any:
    book_database = load_book_database()
    if index < 0 or index >= len(book_database):
        return None

    return book_database[index]


def get_book_by_book_id(book_id: str) -> dict | None:
    book_database = load_book_database()
    for book in book_database:
        if book.get("book_id") == book_id:
            return book

    return None


def check_book_id(book_id: str) -> int | None:
    book_database = load_book_database()
    for index, book in enumerate(book_database):
        if book.get("book_id") == book_id:
            return index
    return None


def add_book(book: dict, db_session: Session) -> bool:
    book_created = create_book(book, db_session)

    if book_created:
        book_database = load_book_database()
        book_database.append(book)
        write_json(book_database)
        book_created = True

    return book_created


def add_book_by_csv(db_session: Session) -> dict:
    try:
        books = read_csv()
        count_books_created = 0

    except Exception as error:
        return {"error csv": str(error)}

    book_database = load_book_database()
    for book in books:
        try:
            print(book)
            ValidationRulesBookCsv.invalid_book_name(book.get('book_name'))
            ValidationRulesBookCsv.invalid_price(float(book.get('price')))
            ValidationRulesBookCsv.invalid_genre(book.get('genre'))
            ValidationRulesBookCsv.book_already_exist(book.get('book_name'), book_database)

            new_book = BookCreateOut(**book)

            book_json_response = jsonable_encoder(new_book)
            book_created = create_book(book_json_response, db_session)

            if book_created:
                count_books_created += 1
                write_csv(book_json_response)
                book_database.append(book_json_response)
                write_json(book_database)

        except BookExceptionCsv as error:
            print(error)
            write_log(book, str(error))

    return {"total_rows": len(books), "total_rows_inserted": count_books_created}


def delete_book_list(book_id: str, db: Session) -> bool:
    excluded = False
    book_database = load_book_database()
    index = check_book_id(book_id)

    if index is not None:
        book_excluded = delete_book(book_id, db)
        if book_excluded:
            del book_database[index]

            write_json(book_database)
            excluded = True

    return excluded


def save_book_changes(book_id: str, book: dict, db: Session) -> Optional[dict]:
    book_updated = update_book_crud(book_id, book, db)
    if book_updated is not None or book_updated:
        book_database = load_book_database()
        index = check_book_id(book_id)
        if index is not None:
            book_database[index].update(book)
            write_json(book_database)
            return book_database[index]

    return None


def update_book_dict(book_id: str, book: dict, db: Session) -> Optional[dict] | None:
    return save_book_changes(book_id, book, db)


def replace_book_dict(book_id: str, book: dict, db: Session) -> Optional[dict]:
    return save_book_changes(book_id, book, db)
