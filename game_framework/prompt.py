from dataclasses import dataclass, field

@dataclass
class Prompt:
    messages: list[dict] = field(default_factory=list)
    tools: list[dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Goal:
    priority: int
    name: str
    description: str