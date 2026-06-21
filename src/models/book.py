from sqlalchemy import Column, String, Integer
from src.database.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String(200), nullable=False)
    price = Column(Integer, nullable=False)
    genre = Column(String(20), nullable=False)
