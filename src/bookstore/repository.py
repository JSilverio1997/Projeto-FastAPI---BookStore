from src.bookstore.utils import read_json, write_json
from typing import Any, Optional

BOOK_PATH = "books.json"
book_database = read_json(r"C:\Users\João\PycharmProjects\fastApi1HoraCurso\books.json")


def get_all_books() -> list:
    return book_database


def get_book_by_index(index: int) -> Any:
    if index < 0 or index >= len(book_database):
        return None

    return book_database[index]


def add_book(book: dict) -> None:
    book_database.append(book)
    write_json(r"books.json", book_database)


def check_book_id(book_id: str) -> Optional[int]:
    index = None
    for i, book in enumerate(book_database):
        if book['book_id'] == book_id:
            index = i

    return index


def delete_book_list(book_id: str) -> bool:
    excluded = False
    index = check_book_id(book_id)

    if index is not None:
        del book_database[index]
        write_json(r"books.json", book_database)
        excluded = True

    return excluded


def update_book_dict(book_id: str, book: dict) -> Optional[dict]:
    index = check_book_id(book_id)
    if index is not None:
        book_database[index].update(book)
        write_json(r"books.json", book_database)
        return book_database[index]

    return None


def replace_book_dict(book_id: str, book: dict) -> Optional[dict]:
    index = check_book_id(book_id)
    if index is not None:
        book_database[index].update(book)
        write_json(r"books.json", book_database)
        return book_database[index]

    return None
