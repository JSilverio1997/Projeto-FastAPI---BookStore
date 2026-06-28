from src.schemas.book import BookCreate, GenreEnum


class RuleBookException:

    @staticmethod
    def index_book_not_found(index: int, book: dict):
        if not book:
            return f"Book at index {index} not found."
        return None

    @staticmethod
    def book_not_found(book: dict):
        if not book:
            return "Book not found."
        return None

    @staticmethod
    def book_list_empty(book: list):
        if not book:
            return "Book List is Empty."
        return None

    @staticmethod
    def book_already_exist(book_name: str, books: list):
        if book_name:
            if any(book.get("book_name").upper() == book_name.upper() for book in books):
                return "This book already exist in the list."

        return None

    @staticmethod
    def book_id_not_found(book_id: str):
        return f"Book with id '{book_id}' does not exist."

    @staticmethod
    def invalid_book_name(book: BookCreate):
        if book.book_name is not None:
            if not book.book_name.strip():
                return "The Book name must be to fill."
        return None

    @staticmethod
    def invalid_price(book: BookCreate):
        if book.price is not None:
            if book.price <= 0:
                return "The price is not allow to be less or equal 0."
        return None

    @staticmethod
    def invalid_genre(book: BookCreate):
        if book.genre is not None:
            if book.genre not in (GenreEnum.FICTION, GenreEnum.NO_FICTION):
                return "The genre field is not allow to be empty and values must be Fiction or Non_Fiction."

        return None
