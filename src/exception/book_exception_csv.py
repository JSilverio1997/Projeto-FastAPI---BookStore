from src.exception.rules_book_exception import RuleBookException


class BookExceptionCsv(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ValidationRulesBookCsv:

    @staticmethod
    def index_book_not_found(index: int, book: dict):
        exception_message = RuleBookException.index_book_not_found(index, book)
        if exception_message is not None:
            raise BookExceptionCsv(exception_message)

    @staticmethod
    def book_not_found(book: dict):
        exception_message = RuleBookException.book_not_found(book)
        if exception_message is not None:
            raise BookExceptionCsv(exception_message)

    @staticmethod
    def book_list_empty(book: list):
        exception_message = RuleBookException.book_list_empty(book)
        if exception_message is not None:
            raise BookExceptionCsv(exception_message)

    @staticmethod
    def book_already_exist(book_name: str, books: list):
        exception_message = RuleBookException.book_already_exist(book_name, books)
        if exception_message is not None:
            raise BookExceptionCsv(exception_message)

    @staticmethod
    def book_id_not_found(book_id: str):
        exception_message = RuleBookException.book_id_not_found(book_id)
        if exception_message is not None:
            raise BookExceptionCsv(exception_message)

    @staticmethod
    def invalid_book_name(book_name: str):
        exception_message = RuleBookException.invalid_book_name(book_name)
        if exception_message is not None:
            raise BookExceptionCsv(exception_message)

    @staticmethod
    def invalid_price(price: float):
        exception_message = RuleBookException.invalid_price(price)
        if exception_message is not None:
            raise BookExceptionCsv(exception_message)

    @staticmethod
    def invalid_genre(genre: str):
        exception_message = RuleBookException.invalid_genre(genre)
        if exception_message is not None:
            raise BookExceptionCsv(exception_message)
