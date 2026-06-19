import random


from fastapi.encoders import jsonable_encoder
from src.repositories.repository import (get_all_books,
                                         get_book_by_index,
                                         add_book,
                                         delete_book_list,
                                         update_book_dict,
                                         replace_book_dict,
                                         get_book_by_book_id)
from src.schemas.schemas import BookIn, BookOut, BookUpdate
from src.exception.book_exception import BookException


def list_all_books(book_name: str, genre: str) -> list[BookOut] | BookOut:
    books = get_all_books()
    BookException.book_list_empty(books)

    list_book_outs = []
    for book in books:
        book_out = BookOut(**book)

        if book_name and genre:
            if (str(book.get("book_name")).upper() == book_name.upper() and
                    str(book.get("genre")).upper() == genre.upper()):
                return book_out

        elif book_name:
            if str(book.get("book_name")).upper() == book_name.upper():
                return book_out

        elif genre:
            if str(book.get("genre")).upper() == genre.upper():
                list_book_outs.append(book_out)
        else:
            list_book_outs.append(book_out)

    BookException.book_list_empty(list_book_outs)

    return list_book_outs
    # return [BookOut(**book) for book in books]


def list_paginate_books(page: int, size: int):
    start = (page - 1) * size
    end = start + size
    books = get_all_books()

    books_items = {"page": page, "size": size, "total": len(books), "data": books[start:end]}
    BookException.book_list_empty(books[start:end])

    return books_items


def list_book_by_position(index: int) -> BookOut:
    book = get_book_by_index(index)
    BookException.index_book_not_found(index, book)
    return BookOut(**book)


def return_book_by_book_id(book_id: str) -> BookOut:
    book = get_book_by_book_id(book_id)
    BookException.book_not_found(book)
    return BookOut(**book)


def list_random_book() -> BookOut:
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
    if excluded is False:
        BookException.book_id_not_found(book_id)


def update_book(book_id: str, book_update: BookUpdate) -> BookOut:
    books = get_all_books()

    BookException.invalid_book_name(book_update)
    BookException.book_already_exist(book_update.book_name, books)
    BookException.invalid_price(book_update)
    BookException.invalid_genre(book_update)

    updated_book = update_book_dict(book_id, book_update.dict(exclude_unset=True))
    if updated_book is not None:
        return BookOut(**updated_book)
    else:
        BookException.book_id_not_found(book_id)


def replace_book(book_id: str, book: BookIn) -> BookOut:
    books = get_all_books()

    BookException.invalid_book_name(book)
    BookException.book_already_exist(book.book_name, books)
    BookException.invalid_genre(book)
    BookException.invalid_price(book)

    replaced_book = replace_book_dict(book_id, book.dict())
    if replaced_book is not None:
        return BookOut(**replaced_book)

    BookException.book_id_not_found(book_id)
