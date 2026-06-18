from typing import Any
from fastapi import APIRouter
from src.schemas.schemas import BookIn, BookOut, BookUpdate
from src.services.services import (list_all_books, list_book_by_position, list_random_book, add_new_book, remove_book,
                                   update_book, replace_book)

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", summary="List of the books", status_code=200, description="Returns the complete list of "
                                                                           "books currently stored in the "
                                                                           "system. Useful for viewing the "
                                                                           "entire catalog")
async def list_books() -> list[BookOut]:
    return list_all_books()


@router.get("/random", summary="Retrieve a random book", status_code=200,
            description="Returns a randomly selected book from the catalog. Useful for quick suggestions or testing.")
async def get_random_book() -> BookOut:
    return list_random_book()

@router.get("/{index}", summary="Retrieve a book by index", status_code=200,
            description=" Retrieves a book from the list based on its index position. If the index does not exist, "
                        "a 404 error is returned.")
async def list_book_by_index(index: int) -> BookOut:
    return list_book_by_position(index)


@router.post("/", summary="Add a book for repositories", status_code=201, description="Adds a new book to "
                                                                                      "the database if it does "
                                                                                      "not already exist.")
async def create_book(book_in: BookIn) -> BookOut:
    return add_new_book(book_in)


@router.patch("/{book_id}", summary="Update some attributes a book", status_code=200,
              description="Updates one or more attributes of an existing book. Uses exclude_unset=True to apply partial"
                          " updates. If the book does not exist, a 404 error is returned.")
async def update_attributes_book(book_id: str, book_update: BookUpdate) -> BookOut:
    return update_book(book_id, book_update)


@router.put("/{book_id}", summary="Replace a old book by new book", status_code=200,
            description="Fully replaces the details of an existing book with new data. Requires a complete payload. "
                        "If the book does not exist, a 404 error is returned.")
async def update_replace_book(book_id: str, new_book: BookIn) -> BookOut:
    return replace_book(book_id, new_book)


@router.delete("/{book_id}", summary="Delete a Book", status_code=204,
               description="Removes a book from the database. Returns status code 204 (No Content) if successful. "
                           "If the book does not exist, a 404 error is returned.")
async def delete_book(book_id: str) -> None:
    return remove_book(book_id)
