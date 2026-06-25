import json
import os.path
import os
from dotenv import load_dotenv
from typing import Any
from rich.console import Console

load_dotenv()
BOOK_PATH = os.getenv("BOOK_PATH")

console = Console()


def write_json(book_list:  list[dict[str, Any]]) -> None:
    try:
        with open(fr"{BOOK_PATH}", mode="w", encoding="utf-8") as json_file:
            json.dump(book_list, json_file)

        console.print(f"The Book Json was created at {BOOK_PATH}.")

    except FileNotFoundError as e:
        console.print(e)
    except Exception as exception:
        console.print(exception)


def read_json() -> list[dict[str, Any]]:
    datas = []
    if os.path.exists(BOOK_PATH):
        with open(fr"{BOOK_PATH}", mode="r", encoding="utf-8") as json_file:
            datas = json.load(json_file)

    else:
        console.print(f"The file not found. {BOOK_PATH}")
    return datas
