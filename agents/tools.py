from core.action import register_tool

import os

@register_tool(tags=["file_operations", "read"])
def read_project_file(name: str) -> str:
    """Reads a file from the project."""
    with open(name, "r") as f:
        return f.read()


@register_tool(tags=["file_operations", "write"])
def write_project_file(name: str, content: str) -> str:
    """Writes content to a file in the project, overwriting it if it already exists."""
    with open(name, "w", encoding="utf-8") as f:
        f.write(content)

    return f"Wrote {len(content)} characters to {name}"


@register_tool(tags=["file_operations", "list"])
def list_project_files() -> list[str]:
    """Lists all files in the project."""
    ignored_dirs = {".venv", ".git", "__pycache__", "logs", "data"}
    ignored_files = {"__init__.py"}
    files = []

    for root, dirs, names in os.walk("."):
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        for name in names:
            if name.endswith(".py") and name not in ignored_files:
                files.append(os.path.relpath(os.path.join(root, name), "."))

    return sorted(files)


@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """Terminates the session and prints the message to the user."""
    return f"{message}\nTerminating..."
