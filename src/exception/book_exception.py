from fastapi import HTTPException
from src.bookstore.schemas import BookIn, BookUpdate, GenreEnum


class BookException:

    @staticmethod
    def book_not_found(book: dict):
        if not book:
            raise HTTPException(status_code=404, detail="Book not found.")

    @staticmethod
    def book_list_empty(book: list):
        if not book:
            raise HTTPException(status_code=404, detail="Book List is Empty.")

    @staticmethod
    def book_already_exist(book_name: str, books: list):
        if book_name:
            if book_name.upper() in books.__str__().upper():
                raise HTTPException(status_code=400, detail="This book already exist in the list.")

    @staticmethod
    def book_id_not_found(book_id: str):
        raise HTTPException(status_code=404, detail=f"This book id {book_id} not exist.")

    @staticmethod
    def invalid_book_name(book: BookIn):
        if book.book_name is not None:
            if not book.book_name.strip():
                raise HTTPException(status_code=400, detail="The Book name must be to fill.")

    @staticmethod
    def invalid_price(book: BookIn):
        if book.price is not None:
            if book.price <= 0:
                raise HTTPException(status_code=400, detail="The price is not allow to be less or equal 0.")

    @staticmethod
    def invalid_genre(book: BookIn):
        if book.genre is not None:
            if book.genre not in (GenreEnum.FICTION, GenreEnum.NO_FICTION):
                raise HTTPException(status_code=400, detail="The genre field is not allow to be empty and values must "
                                                            "be Fiction or Non_Fiction.")
