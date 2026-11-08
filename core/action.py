from dataclasses import dataclass, field
from typing import Callable

@dataclass
class Action:
    name: str
    function: Callable
    description: str
    parameters: dict
    terminal: bool

    def execute(self, **args):
        return self.function(**args)


@dataclass
class ActionRegistry:
    actions: dict = field(default_factory=dict)

    def register(self, action: Action):
        self.actions[action.name] = action


    def get_call_actions(self, action_names: list[str]) -> list[Action | None]:
        return [
            self.actions.get(action_name, None)
            for action_name in action_names
        ]


    def get_available_actions(self) -> list[Action]:
        return list(self.actions.values())