from sqlalchemy import Column, String, Float, DateTime, func, text
from src.database.database import Base


class Book(Base):
    __tablename__ = "books"

    book_id = Column(String(500), primary_key=True, index=True)
    book_name = Column(String(200), nullable=False, unique=True)
    price = Column(Float, nullable=False)
    genre = Column(String(20), nullable=False)
    created_date = Column(DateTime, nullable=True, default=func.now())
    updated_date = Column(DateTime, nullable=False,server_onupdate=text("CURRENT_TIMESTAMP"))
