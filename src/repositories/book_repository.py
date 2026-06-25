from src.utils.utils import read_json, write_json
from typing import Any, Optional
from src.crud.book_crud import create_book, delete_book, update_book_crud
from sqlalchemy.orm import Session


BOOK_PATH = r"C:\Users\João\PycharmProjects\fastApi1HoraCurso\books.json"
book_database = read_json(BOOK_PATH)


def get_all_books() -> list[dict]:
    return book_database


def get_book_by_index(index: int) -> Any:
    if index < 0 or index >= len(book_database):
        return None

    return book_database[index]


def get_book_by_book_id(book_id: str) -> dict | None:
    for book in book_database:
        if book.get("book_id") == book_id:
            return book

    return None


def check_book_id(book_id: str) -> int | None:
    for index, book in enumerate(book_database):
        if book.get("book_id") == book_id:
            return index
    return None


def add_book(book: dict, db_session: Session) -> bool:
    book_created = create_book(book, db_session)

    if book_created:
        book_database.append(book)
        write_json(BOOK_PATH, book_database)
        book_created = True

    return book_created


def delete_book_list(book_id: str, db: Session) -> bool:
    excluded = False
    index = check_book_id(book_id)

    if index is not None:
        book_excluded = delete_book(book_id, db)
        if book_excluded:
            del book_database[index]

            write_json(BOOK_PATH, book_database)
            excluded = True

    return excluded


def save_book_changes(book_id: str, book: dict, db: Session) -> Optional[dict]:
    book_updated = update_book_crud(book_id, book, db)
    if book_updated is not None or book_updated:
        index = check_book_id(book_id)
        if index is not None:
            book_database[index].update(book)
            write_json(BOOK_PATH, book_database)
            return book_database[index]

    return None


def update_book_dict(book_id: str, book: dict, db: Session) -> Optional[dict] | None:
    return save_book_changes(book_id, book, db)


def replace_book_dict(book_id: str, book: dict, db: Session) -> Optional[dict]:
    return save_book_changes(book_id, book, db)
