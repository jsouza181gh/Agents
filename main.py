import os

from game_framework.llm import generate_response
from game_framework.language import AgentFunctionCallingActionLanguage
from game_framework.action import ActionRegistry, Action
from game_framework.environment import Environment
from game_framework.prompt import Goal
from game_framework.agent import Agent

goals = [
    Goal(priority=1, name="Gather Information", description="Read each file in the project"),
    Goal(priority=1, name="Terminate", description="Call the terminate call when you have read all the files "
                                                    "and provide the content of the README in the terminate message")
]

agent_language = AgentFunctionCallingActionLanguage()

def read_project_file(name: str) -> str:
    with open(name, "r") as f:
        return f.read()

def list_project_files() -> list[str]:
    return sorted([file for file in os.listdir(".") if file.endswith(".py")])


action_registry = ActionRegistry()
action_registry.register(Action(
    name="list_project_files",
    function=list_project_files,
    description="lists all files in the project.",
    parameters={},
    terminal=False
))
action_registry.register(Action(
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
))
action_registry.register(Action(
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
))

environment = Environment()

agent = Agent(goals, agent_language, action_registry, generate_response, environment)

user_input = "Write a README for this project."
final_memory = agent.run(user_input)

print(final_memory.get_memories())