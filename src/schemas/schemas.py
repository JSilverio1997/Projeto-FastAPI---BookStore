import uuid
from src.enums.GenreEnum import GenreEnum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class BookIn(BaseModel):
    book_name: str
    price: float
    genre: GenreEnum

    @field_validator("book_name")
    def book_name_not_null(cls, book_name: str):
        if book_name is None:
            raise ValueError("It is not allow the null  for book name field.")

        return book_name.strip()

    @field_validator("price")
    def price_not_null(cls, value: float):
        if value is None:
            raise ValueError("It is not allow the null  for price field.")

        return value

    @field_validator("genre")
    def genre_not_null(cls, genre: GenreEnum):
        if genre is None:
            raise ValueError("It is not allow the null  for genre field.")

        return genre


class BookOut(BookIn):
    book_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4().hex))


class BookUpdate(BookIn):
    book_name: Optional[str] = None
    price: Optional[float] = None
    genre: Optional[GenreEnum] = None



