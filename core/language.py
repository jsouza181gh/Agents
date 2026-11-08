from core.models import AssistantMessage, ToolCall, Prompt
from core.memory import Memory
from core.action import Action
from core.goal import Goal

from abc import ABC, abstractmethod
import logging
import json

class AgentLanguage(ABC):
    @abstractmethod
    def construct_prompt(
        self,
        memory: Memory,
        goals: list[Goal],
        actions: list[Action]
    ) -> Prompt: ...


    @abstractmethod
    def parse_response(
        self,
        response: list[AssistantMessage]
    ) -> list[ToolCall]: ...


class GAMEFrameworkLanguage(AgentLanguage):
    logger = logging.getLogger(__name__)

    def format_goals(self, goals: list[Goal]) -> list:
        sep = "\n-------------------\n"
        goal_instructions = "\n\n".join([f"{goal.name}:{sep}{goal.description}{sep}" for goal in goals])
        
        return [
            {
                "role": "system", 
                "content": goal_instructions
            }
        ]


    def format_memory(self, memory: Memory) -> list:
        items = memory.get_memories()
        mapped_items = []
        for item in items:

            mapped_item = dict(item)

            if not mapped_item.get("content") and not mapped_item.get("tool_calls"):
                mapped_item["content"] = json.dumps(item, indent=4)

            mapped_items.append(mapped_item)

        return mapped_items


    def format_actions(self, actions: list[Action]) -> list:
        tools = [
            {
                "type": "function",
                "function": {
                    "name": action.name,
                    "description": action.description,
                    "parameters": action.parameters,
                },
            } for action in actions
        ]

        return tools


    def construct_prompt(
        self,
        memory: Memory,
        goals: list[Goal],
        actions: list[Action]
    ) -> Prompt:
        prompt = []
        prompt += self.format_goals(goals)
        prompt += self.format_memory(memory)
        tools = self.format_actions(actions)
        
        return Prompt(messages=prompt, tools=tools)


    def parse_response(self, response: list[AssistantMessage]) -> list[ToolCall]:
        received_tools = []

        for message in response:
            if message.tool_calls:
                received_tools.extend(message.tool_calls)
            elif not message.content:
                self.logger.warning("Ignoring empty assistant message: no content and no tool calls.")
            else:
                received_tools.append(
                    ToolCall(
                        function_name="terminate",
                        args={"message": message.content}
                    )
                )

        return received_tools