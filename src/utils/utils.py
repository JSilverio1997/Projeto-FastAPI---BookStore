import json
import os.path
from typing import Any

from rich.console import Console

console = Console()


def write_json(path: str, book_list:  list[dict[str, Any]]) -> None:
    try:
        with open(fr"{path}", mode="w", encoding="utf-8") as json_file:
            json.dump(book_list, json_file)

        console.print(f"The Book Json was created at {path}.")

    except FileNotFoundError as e:
        console.print(e)
    except Exception as exception:
        console.print(exception)


def read_json(path: str) -> list[dict[str, Any]]:
    datas = []
    if os.path.exists(path):
        with open(fr"{path}", mode="r", encoding="utf-8") as json_file:
            datas = json.load(json_file)

    else:
        console.print(f"The file not found. {path}")
    return datas
