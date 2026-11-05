from litellm import completion, ModelResponse
from litellm.types.utils import ChatCompletionMessageToolCall
from typing import cast
import json

from game_framework.prompt import Prompt

def generate_response(prompt: Prompt) -> str:
    """Call LLM to get response"""

    messages = prompt.messages
    tools = prompt.tools

    result: str | None = None

    if not tools:
        response = cast(
            ModelResponse,
            completion(
                model="gemini/gemini-3.1-flash-lite",
                messages=messages,
                max_tokens=1024
            )
        )
        result = response.choices[0].message.content
    else:
        response = cast(
            ModelResponse,
            completion(
                model="gemini/gemini-3.1-flash-lite",
                messages=messages,
                tools=tools,
                max_tokens=1024
            )
        )

        tool_calls = response.choices[0].message.tool_calls
        tool = tool_calls[0] if tool_calls else None
        if isinstance(tool, ChatCompletionMessageToolCall):
            result = json.dumps({
                "tool": tool.function.name,
                "args": json.loads(tool.function.arguments),
            })
        else:
            result = response.choices[0].message.content

    return result or ""
