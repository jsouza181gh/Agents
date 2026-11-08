from config import MAX_ITERATIONS
from core.models import AssistantMessage, ToolCall, Prompt
from core.language import AgentLanguage
from core.action import ActionRegistry, Action
from core.environment import Environment
from core.memory import Memory
from core.goal import Goal

from dataclasses import dataclass
from typing import Callable
import json

@dataclass
class Agent:
    goals: list[Goal]
    actions: ActionRegistry
    environment: Environment
    agent_language: AgentLanguage
    generate_response: Callable[[Prompt], list[AssistantMessage]]

    def construct_prompt(
        self,
        goals: list[Goal],
        memory: Memory,
        actions: ActionRegistry
    ) -> Prompt:
        return self.agent_language.construct_prompt(
            actions=actions.get_available_actions(),
            goals=goals,
            memory=memory
        )


    def get_actions(self, response: list[AssistantMessage]) -> list[tuple[Action | None, ToolCall]]:
        tool_calls = self.agent_language.parse_response(response)

        tools = [
            tool_call.function_name
            for tool_call in tool_calls
        ]

        actions = self.actions.get_call_actions(tools)

        return [
            (action, tool_call)
            for action, tool_call in zip(actions, tool_calls)
        ]


    def should_terminate(self, pairs: list[tuple[Action | None, ToolCall]]) -> bool:
        return any(
            action.terminal
            for action, _ in pairs
            if action is not None
        )


    def set_current_task(self, memory: Memory, task: str):
        memory.add_memory({"role": "user", "content": task})


    def update_memory(
        self,
        memory: Memory,
        response: list[AssistantMessage],
        tool_calls: list[ToolCall],
        results: list[dict]
    ):
        for message in response:
            if message.tool_calls:
                memory.add_memory({
                    "role": "assistant",
                    "content": message.content,
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_call.function_name,
                                "arguments": json.dumps(tool_call.args)
                            }
                        }
                        for tool_call in message.tool_calls
                    ]
                })
            elif message.content:
                memory.add_memory({"role": "assistant", "content": message.content})

        for tool_call, result in zip(tool_calls, results):
            if tool_call.id:
                memory.add_memory({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
            else:
                memory.add_memory({"role": "user", "content": json.dumps(result)})


    def prompt_llm_for_action(self, full_prompt: Prompt) -> list[AssistantMessage]:
        response = self.generate_response(full_prompt)
        return response


    def run(self, user_input: str, memory=None, max_iterations: int = MAX_ITERATIONS) -> Memory:
        memory = memory or Memory()
        self.set_current_task(memory, user_input)

        for _ in range(max_iterations):
            prompt = self.construct_prompt(self.goals, memory, self.actions)

            print("Agent thinking...")
            response = self.prompt_llm_for_action(prompt)
            print(f"Agent Decision: {response}")

            pairs = self.get_actions(response)

            results = [
                self.environment.execute_action(action, tool_call.args)
                for action, tool_call in pairs
            ]

            print(f"Action Result: {results}")

            tool_calls = [tool_call for _, tool_call in pairs]
            self.update_memory(memory, response, tool_calls, results)

            if self.should_terminate(pairs):
                break

        return memory