from core.action import Action

import os

def read_project_file(name: str) -> str:
    with open(name, "r") as f:
        return f.read()


def write_project_file(name: str, content: str) -> str:
    with open(name, "w", encoding="utf-8") as f:
        f.write(content)

    return f"Wrote {len(content)} characters to {name}"


def list_project_files() -> list[str]:
    ignored_dirs = {".venv", ".git", "__pycache__", "logs", "data"}
    ignored_files = {"__init__.py"}
    files = []

    for root, dirs, names in os.walk("."):
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        for name in names:
            if name.endswith(".py") and name not in ignored_files:
                files.append(os.path.relpath(os.path.join(root, name), "."))

    return sorted(files)


LIST_PROJECT_FILES = Action(
    name="list_project_files",
    function=list_project_files,
    description="Lists all files in the project.",
    parameters={},
    terminal=False
)

READ_PROJECT_FILE = Action(
    name="read_project_file",
    function=read_project_file,
    description="Reads a file from the project.",
    parameters={
        "type": "object",
        "properties": {
            "name": {"type": "string"}
        },
        "required": ["name"]
    },
    terminal=False
)

WRITE_PROJECT_FILE = Action(
    name="write_project_file",
    function=write_project_file,
    description="Writes content to a file in the project, overwriting it if it already exists.",
    parameters={
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "content": {"type": "string"}
        },
        "required": ["name", "content"]
    },
    terminal=False
)

TERMINATE = Action(
    name="terminate",
    function=lambda message: f"{message}\nTerminating...",
    description="Terminates the session and prints the message to the user.",
    parameters={
        "type": "object",
        "properties": {
            "message": {"type": "string"}
        },
        "required": []
    },
    terminal=True
)
