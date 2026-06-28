import json
import os.path
import os
from csv import DictReader
from dotenv import load_dotenv
from typing import Any
from rich.console import Console
import csv
from datetime import datetime
from src.schemas.book import BookDb

load_dotenv()
BOOK_PATH_JSON = os.getenv("BOOK_PATH_JSON")
BOOK_PATH_CSV = os.getenv("BOOK_PATH_CSV")

console = Console()


def write_json(book_list: list[dict[str, Any]]) -> None:
    try:
        with open(fr"{BOOK_PATH_JSON}", mode="w", encoding="utf-8") as json_file:
            json.dump(book_list, json_file)

        console.print(f"The Book Json was created at {BOOK_PATH_JSON}.")

    except FileNotFoundError as e:
        console.print(e)
    except Exception as exception:
        console.print(exception)


def read_json() -> list[dict[str, Any]]:
    datas = []
    if os.path.exists(BOOK_PATH_JSON):
        with open(fr"{BOOK_PATH_JSON}", mode="r", encoding="utf-8") as json_file:
            datas = json.load(json_file)

    else:
        console.print(f"The file not found. {BOOK_PATH_JSON}")
    return datas


def write_csv(books: list[dict[str, Any]]) -> None:
    try:
        header = books[0].keys()
        current_datetime = datetime.now().strftime("%d%m%Y%H%M%S")
        path = rf"{BOOK_PATH_CSV}\books_{current_datetime}.csv"

        with open(path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=header, delimiter=";")
            writer.writeheader()
            writer.writerows(books)

        console.print(f"The file created in the path {BOOK_PATH_CSV}")

    except Exception as e:
        console.print(e)


def read_csv() -> list:
    try:
        with open(rf"{BOOK_PATH_CSV}/books.csv", mode="r", newline="", encoding="utf-8") as read_csv:
            books_csv = csv.DictReader(read_csv, delimiter=";")

            datas_list = []
            for book in books_csv:
                datas_list.append(book)

        return datas_list

    except FileNotFoundError as error:
        console.print(error)

    except Exception as error:
        console.print(error)


if __name__ == "__main__":
    # write_csv(read_json())
    data_list = read_csv()
    console.print(data_list)

