import os
from collections.abc import Callable
from typing import TypedDict, NotRequired

class ToolResult(TypedDict):
    result: NotRequired[str | list[str]]
    error: NotRequired[str]


def list_files() ->  ToolResult:
    return {"result": os.listdir("informations")}


def read_file(file_name: str) -> ToolResult:
    with open(f"informations/{file_name}", encoding="utf-8") as file:
        try: 
            content = file.read()
            return {"result": content}

        except FileNotFoundError:
            return {"error": f"The file {file_name}, was not found."}

        except Exception as e:
            return {"error": f"The file {file_name}, could not be readed.\n{e}"}


def terminate(task: str) -> ToolResult:
    print(f"Resultado Final: {task}")
    return {"result": "The loop is finished."}


TOOLS: dict[str, Callable[..., ToolResult]] = {
    "list_files" : list_files,
    "read_file" : read_file,
    "terminate" : terminate
}