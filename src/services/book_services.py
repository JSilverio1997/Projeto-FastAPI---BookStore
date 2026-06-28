import random
from fastapi.encoders import jsonable_encoder
from src.repositories.book_repository import (get_all_books,
                                              get_book_by_index,
                                              add_book,
                                              delete_book_list,
                                              update_book_dict,
                                              replace_book_dict,
                                              get_book_by_book_id,
                                              add_book_by_csv)
from src.schemas.book import BookCreate, BookCreateOut, BookPatch, BookPut, BookResponse, BookPaginatedResponse, \
    BookCreatedByCsv
from src.exception.book_exception_http import BookException
from sqlalchemy.orm import Session


def list_all_books(book_name: str, genre: str) -> list[BookResponse] | BookResponse:
    books = get_all_books()
    BookException.book_list_empty(books)

    list_book_outs = []
    for book in books:
        book_response = BookResponse(**book)

        if book_name and genre:
            if (str(book.get("book_name")).upper() == book_name.upper() and
                    str(book.get("genre")).upper() == genre.upper()):
                return book_response

        elif book_name:
            if str(book.get("book_name")).upper() == book_name.upper():
                return book_response

        elif genre:
            if str(book.get("genre")).upper() == genre.upper():
                list_book_outs.append(book_response)
        else:
            list_book_outs.append(book_response)

    BookException.book_list_empty(list_book_outs)

    return list_book_outs
    # return [BookOut(**book) for book in books]


def list_paginate_books(page: int, size: int) -> BookPaginatedResponse:
    start = (page - 1) * size
    end = start + size
    books = get_all_books()

    books_items = BookPaginatedResponse(
        page=page,
        size=size,
        total=len(books),
        data=[BookCreateOut(**book) for book in books[start:end]]
    )
    BookException.book_list_empty(books[start:end])

    return books_items


def list_book_by_position(index: int) -> BookResponse:
    book = get_book_by_index(index)
    BookException.index_book_not_found(index, book)
    return BookResponse(**book)


def return_book_by_book_id(book_id: str) -> BookResponse:
    book = get_book_by_book_id(book_id)
    BookException.book_not_found(book)
    return BookResponse(**book)


def list_random_book() -> BookResponse:
    book_random = get_all_books()
    BookException.book_list_empty(book_random)

    return random.choice(book_random)


def add_new_book(book_in: BookCreate, db_session: Session) -> BookCreateOut:
    books = get_all_books()

    BookException.invalid_book_name(book_in)
    BookException.invalid_genre(book_in)
    BookException.invalid_price(book_in)

    BookException.book_already_exist(book_in.book_name, books)
    book_response = BookCreateOut(**book_in.dict())
    book_json_response = jsonable_encoder(book_response)

    book_created = add_book(book_json_response, db_session)

    if book_created:
        return book_response


def add_new_book_by_csv(db_session: Session) -> BookCreatedByCsv | None:
    books = add_book_by_csv(db_session)
    if books is not None:
        books_created = BookCreatedByCsv(**books)
        print(books)
        return books_created

    return None


def remove_book(book_id: str, db: Session) -> None:
    excluded = delete_book_list(book_id, db)
    # if excluded:
    #     return {"message": f"The book {book_id} was deleted."}
    #
    if excluded is False:
        BookException.book_id_not_found(book_id)


def update_book_service(book_id: str, book_update: BookPatch, db: Session) -> BookResponse:
    books = get_all_books()

    BookException.invalid_book_name(book_update)
    BookException.book_already_exist(book_update.book_name, books)
    BookException.invalid_price(book_update)
    BookException.invalid_genre(book_update)

    updated_book = update_book_dict(book_id, book_update.dict(exclude_unset=True), db)
    if updated_book is not None:
        BookResponse.book_id = book_id
        return BookResponse(**updated_book)
    else:
        BookException.book_id_not_found(book_id)


def replace_book(book_id: str, book: BookPut, db: Session) -> BookResponse:
    books = get_all_books()

    BookException.invalid_book_name(book)
    BookException.book_already_exist(book.book_name, books)
    BookException.invalid_genre(book)
    BookException.invalid_price(book)

    replaced_book = replace_book_dict(book_id, book.dict(), db)
    if replaced_book is not None:
        return BookResponse(**replaced_book)

    BookException.book_id_not_found(book_id)
