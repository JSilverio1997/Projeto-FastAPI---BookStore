from typing import Optional

from starlette import status
from fastapi import APIRouter, Query, Depends
from src.schemas.book import BookCreate, BookCreateOut, BookPatch, BookPut, BookPaginatedResponse
from src.services.book_services import (list_all_books,
                                        list_book_by_position,
                                        list_random_book,
                                        add_new_book,
                                        remove_book,
                                        update_book_service,
                                        replace_book,
                                        return_book_by_book_id,
                                        list_paginate_books)
from sqlalchemy.orm import Session
from src.database.database import get_db

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", summary="List of the books", status_code=status.HTTP_200_OK,
            description="Returns the complete list of books currently stored in the "
                        "system. Useful for viewing the entire catalog",
            response_model=list[BookCreateOut] | BookCreateOut)
async def list_books(book_name: Optional[str] = Query(None, alias="book_name", min_length=1, max_length=150,
                                                      description="book_name"),
                     genre: Optional[str] = Query(None, alias="genre", min_length=1, max_length=150,
                                                  description="genre")) -> list[BookCreateOut] | BookCreateOut:
    return list_all_books(book_name, genre)


@router.get("/random", summary="Retrieve a random book", status_code=status.HTTP_200_OK,
            description="Returns a randomly selected book from the catalog. Useful for quick suggestions or testing.",
            response_model=BookCreateOut)
async def get_random_book() -> BookCreateOut:
    return list_random_book()


@router.get("/index/{index}", summary="Retrieve a book by index", status_code=status.HTTP_200_OK,
            description=" Retrieves a book from the list based on its index position. If the index does not exist, "
                        "a 404 error is returned.",
            response_model=BookCreateOut)
async def list_book_by_index(index: int) -> BookCreateOut:
    book = list_book_by_position(index)
    return book


@router.get("/{book_id}", summary="Retrieve a book using the book id", status_code=status.HTTP_200_OK,
            description="Return the book using the book id as an parameter", response_model=BookCreateOut)
async def get_book_book_id(book_id: str) -> BookCreateOut:
    return return_book_by_book_id(book_id)


@router.get("/items/books", summary="Retrieve all books paginated", status_code=status.HTTP_200_OK,
            description="Return all books using limit and offset", response_model=BookPaginatedResponse)
async def get_all_books_batch(page: int = Query(default=1, ge=1, alias="page_number", description="Page Number"),
                              size: int = Query(default=5, ge=1, alias="page_size", le=5,
                                                description="Quantity of items for page")) -> BookPaginatedResponse:
    return list_paginate_books(page, size)


@router.post("/", summary="Add a book for repositories", status_code=status.HTTP_201_CREATED,
             description="Adds a new book to the database if it does not already exist.", response_model=BookCreateOut)
async def create_book(book_in: BookCreate, db_session: Session = Depends(get_db)) -> BookCreateOut:
    return add_new_book(book_in, db_session)


@router.patch("/{book_id}", summary="Update some attributes a book", status_code=status.HTTP_200_OK,
              description="Updates one or more attributes of an existing book. Uses exclude_unset=True to apply partial"
                          " updates. If the book does not exist, a 404 error is returned.",
              response_model=BookCreateOut)
async def update_attributes_book(book_id: str, book_update: BookPatch, db_session: Session = Depends(get_db)) -> BookCreateOut:
    return update_book_service(book_id, book_update, db_session)


@router.put("/{book_id}", summary="Replace a old book by new book", status_code=status.HTTP_200_OK,
            description="Fully replaces the details of an existing book with new data. Requires a complete payload. "
                        "If the book does not exist, a 404 error is returned.", response_model=BookCreateOut)
async def update_replace_book(book_id: str, new_book: BookPut, db_session: Session = Depends(get_db)) -> BookCreateOut:
    return replace_book(book_id, new_book, db_session)


@router.delete("/{book_id}", summary="Delete a Book", status_code=status.HTTP_204_NO_CONTENT,
               description="Removes a book from the database. Returns status code 204 (No Content) if successful. "
                           "If the book does not exist, a 404 error is returned.", response_model=None)
async def delete_book(book_id: str, db_session: Session = Depends(get_db)) -> None:
    return remove_book(book_id, db_session)
