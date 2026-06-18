from fastapi import FastAPI
from src.services.services import list_all_books
from src.core.router import router as core_router
from src.api.v1.routes import router as books_router

app = FastAPI()
app.include_router(core_router)
app.include_router(books_router)


def main():
    print("Hello from src!")
    list_all_books()


if __name__ == "__main__":
    main()
