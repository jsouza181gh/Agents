from dataclasses import dataclass, field
from typing import Callable, get_origin, get_type_hints
import inspect

JSON_TYPES = {str: "string", int: "integer", float: "number", bool: "boolean", list: "array", dict: "object"}
REGISTERED_ACTIONS: dict = {}

@dataclass
class Action:
    name: str
    function: Callable
    description: str
    parameters: dict
    terminal: bool
    tags: list[str] = field(default_factory=list)

    def execute(self, **args):
        return self.function(**args)


def register_tool(name=None, description=None, terminal=False, tags=None):
    def decorator(func):
        params = inspect.signature(func).parameters
        hints = get_type_hints(func)

        action = Action(
            name=name or func.__name__,
            function=func,
            description=description or inspect.getdoc(func) or "No description provided.",
            parameters={
                "type": "object",
                "properties": {
                    param: {"type": JSON_TYPES.get(get_origin(hints.get(param, str)) or hints.get(param, str), "string")}
                    for param in params
                },
                "required": [
                    param
                    for param, spec in params.items()
                    if spec.default is inspect.Parameter.empty
                ]
            },
            terminal=terminal,
            tags=tags or []
        )
        REGISTERED_ACTIONS[action.name] = action

        return func
    return decorator


@dataclass
class ActionRegistry:
    actions: dict = field(default_factory=dict)
    tags: list[str] | None = None

    def __post_init__(self):
        for action in REGISTERED_ACTIONS.values():
            if self.tags is None or set(self.tags) & set(action.tags):
                self.register(action)


    def register(self, action: Action):
        self.actions[action.name] = action


    def get_call_actions(self, action_names: list[str]) -> list[Action | None]:
        return [
            self.actions.get(action_name, None)
            for action_name in action_names
        ]


    def get_available_actions(self) -> list[Action]:
        return list(self.actions.values())
