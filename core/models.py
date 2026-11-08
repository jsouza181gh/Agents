from dataclasses import dataclass, field

@dataclass
class Prompt:
    messages: list[dict] = field(default_factory=list)
    tools: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class ToolCall:
    function_name: str
    args: dict
    id: str | None = None


@dataclass
class AssistantMessage:
    content: str | None
    role: str
    tool_calls: list[ToolCall] | None
