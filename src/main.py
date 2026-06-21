from fastapi import FastAPI
from src.core.global_router import router as core_router
from src.api.v1.book_routes import router as books_router
from src.database.database import init_db

app = FastAPI()


@app.on_event("startup")
def startup() -> None:
    init_db()


app.include_router(core_router)
app.include_router(books_router)


def main():
    print("Hello from src!")


if __name__ == "__main__":
    main()
