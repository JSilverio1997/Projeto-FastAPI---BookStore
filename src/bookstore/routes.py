from typing import Any
from fastapi import APIRouter
from src.bookstore.schemas import BookIn, BookOut, BookUpdate
from src.bookstore.services import (list_all_books, list_book_by_id, list_random_book, add_new_book, remove_book,
                                    update_book, replace_book)

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/list-books", summary="List of the books", status_code=200)
async def list_books() -> Any:
    return list_all_books()


@router.get("/list-book-by-index/{index}", summary="The Find a book by index", status_code=200)
async def list_book_by_index(index: int) -> dict:
    return list_book_by_id(index)


@router.get("/get-random-book", summary="The Random book ", status_code=200)
async def get_random_book() -> dict:
    return list_random_book()


@router.post("/add-book", summary="Add a book for bookstore", status_code=201)
async def create_book(book_in: BookIn) -> BookOut:
    return add_new_book(book_in)


@router.patch("/update-book/{book_id}", summary="Update some attributes a book", status_code=200)
async def update_attributes_book(book_id: str,  book_update: BookUpdate) -> BookOut:
    return update_book(book_id, book_update)


@router.put("/replace-book/{book_id}", summary="Replace a old book by new book", status_code=200)
async def update_replace_book(book_id: str, new_book: BookIn) -> BookOut:
    return replace_book(book_id, new_book)


@router.delete("/delete-book/{book_id}", summary="Delete a Book", status_code=204)
async def delete_book(book_id: str) -> None:
    return remove_book(book_id)
