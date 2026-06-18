from src.utils.utils import read_json, write_json
from typing import Any, Optional

BOOK_PATH = r"C:\Users\João\PycharmProjects\fastApi1HoraCurso\books.json"
book_database = read_json(BOOK_PATH)


def get_all_books() -> list[dict]:
    return book_database


def get_book_by_index(index: int) -> Any:
    if index < 0 or index >= len(book_database):
        return None

    return book_database[index]


def add_book(book: dict) -> None:
    book_database.append(book)
    write_json(BOOK_PATH, book_database)


def check_book_id(book_id: str) -> int | None:
    for index, book in enumerate(book_database):
        if book['book_id'] == book_id:
            return index
    return None


def delete_book_list(book_id: str) -> bool:
    excluded = False
    index = check_book_id(book_id)

    if index is not None:
        del book_database[index]
        write_json(BOOK_PATH, book_database)
        excluded = True

    return excluded


def save_book_changes(book_id: str, book: dict) -> Optional[dict]:
    index = check_book_id(book_id)
    if index is not None:
        book_database[index].update(book)
        write_json(BOOK_PATH, book_database)
        return book_database[index]

    return None


def update_book_dict(book_id: str, book: dict) -> Optional[dict] | None:
    return save_book_changes(book_id, book)


def replace_book_dict(book_id: str, book: dict) -> Optional[dict]:
    return save_book_changes(book_id, book)
