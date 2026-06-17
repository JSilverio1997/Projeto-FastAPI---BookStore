import json
import os.path
from rich.console import Console

console = Console()


def write_json(path: str, book_list: list[dict]) -> None:
    try:
        with open(fr"{path}", mode="w", encoding="utf-8") as json_file:
            json.dump(book_list, json_file)

        if json_file.closed:
            console.print("The Book Json was created.")

    except (FileExistsError, FileNotFoundError) as e:
        console.print(e)
    except Exception as exception:
        console.print(exception)


def read_json(path: str) -> list[dict]:
    datas = []
    if os.path.exists(path):
        with open(file=fr"{path}", mode="r", encoding="utf-8") as json_file:
            datas = json.load(json_file)

    else:
        console.print(f"não achou o arquivo {os.path} {path}")
    return datas
