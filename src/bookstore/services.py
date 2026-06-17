import random
from typing import Any
from fastapi.encoders import jsonable_encoder
from src.bookstore.repository import (get_all_books, get_book_by_index, add_book, delete_book_list, update_book_dict,
                                      replace_book_dict)
from src.bookstore.schemas import BookIn, BookOut, BookUpdate, GenreEnum
from src.exception.book_exception import BookException


def list_all_books() -> list:
    books = get_all_books()
    BookException.book_list_empty(books)
    return books


def list_book_by_id(index: int) -> dict:
    book = get_book_by_index(index)
    BookException.book_not_found(book)

    return book


def list_random_book() -> dict:
    book_random = get_all_books()
    BookException.book_list_empty(book_random)

    return random.choice(book_random)


def add_new_book(book_in: BookIn) -> BookOut:
    books = get_all_books()

    BookException.invalid_book_name(book_in)
    BookException.invalid_genre(book_in)
    BookException.invalid_price(book_in)

    BookException.book_already_exist(book_in.book_name, books)

    book_out = BookOut(**book_in.dict())
    json_book_out = jsonable_encoder(book_out)

    add_book(json_book_out)

    return book_out


def remove_book(book_id: str) -> None:
    excluded = delete_book_list(book_id)
    # if excluded:
    #     return {"message": f"The book {book_id} was deleted."}
    #
    # BookException.book_id_not_found(book_id)


def update_book(book_id: str, book_update: BookUpdate) -> Any | None:
    books = get_all_books()

    BookException.invalid_book_name(book_update)
    BookException.book_already_exist(book_update.book_name, books)
    BookException.invalid_price(book_update)
    BookException.invalid_genre(book_update)

    updated_book = update_book_dict(book_id, book_update.dict(exclude_unset=True))
    if updated_book is not None:
        return jsonable_encoder(updated_book)
    else:
        BookException.book_id_not_found(book_id)


def replace_book(book_id: str, book: BookIn):
    books = get_all_books()

    BookException.invalid_book_name(book)
    BookException.book_already_exist(book.book_name, books)
    BookException.invalid_genre(book)
    BookException.invalid_price(book)

    replaced_book = replace_book_dict(book_id, book.dict(exclude_unset=True))
    if replaced_book is not None:
        return jsonable_encoder(replaced_book)

    BookException.book_id_not_found(book_id)
