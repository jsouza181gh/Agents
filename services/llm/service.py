from config import LLM_MODEL, MAX_TOKENS, MAX_RETRIES, FREE_TIER, FREE_TIER_RPM
from core.models import Prompt, ToolCall, AssistantMessage

from litellm import completion, ModelResponse
from litellm.types.utils import (
    ChatCompletionMessageToolCall as ChatResponseToolCall,
    CompletionTokensDetailsWrapper as OutputTokensDetails,
    PromptTokensDetailsWrapper as InputTokensDetails,
    Choices,
    Usage,
)
from dataclasses import dataclass, field
from typing import cast
import logging
import time
import json

@dataclass
class LLMService:
    model = LLM_MODEL
    max_tokens = MAX_TOKENS
    max_retries = MAX_RETRIES
    free_tier = FREE_TIER
    min_interval = 60 / FREE_TIER_RPM
    logger = logging.getLogger(__name__)
    last_call_at: float | None = field(default=None, init=False)

    def wait_for_rate_limit(self):
        if not self.free_tier:
            return

        if self.last_call_at is not None:
            remaining = self.min_interval - (time.monotonic() - self.last_call_at)
            if remaining > 0:
                time.sleep(remaining)

        self.last_call_at = time.monotonic()

    def generate_response(self, prompt: Prompt):
        self.wait_for_rate_limit()

        messages = prompt.messages
        tools = prompt.tools

        response = cast(
            ModelResponse,
            completion(
                messages=messages,
                tools=tools,
                model=self.model,
                max_tokens=self.max_tokens,
                num_retries=self.max_retries,
            )
        )

        choices = [
            cast(Choices, choice)
            for choice in response.choices
        ]

        response_messages = [
            choice.message
            for choice in choices
        ]

        assistant_messages = []

        for message in response_messages:
            assistant_message = AssistantMessage(
                content=message.content,
                role=message.role,
                tool_calls=None
            )

            tool_calls = message.tool_calls

            if tool_calls is not None:
                assistant_message.tool_calls = [
                    ToolCall(
                        function_name=str(tool_call.function.name),
                        args=json.loads(tool_call.function.arguments),
                        id=tool_call.id
                    )
                    for tool_call in [
                        cast(ChatResponseToolCall, tool_call)
                        for tool_call in tool_calls
                    ]
                ]

            assistant_messages.append(assistant_message)

        usage = cast(Usage, getattr(response, "usage"))
        input_details = cast(InputTokensDetails, usage.prompt_tokens_details)
        output_details = cast(OutputTokensDetails, usage.completion_tokens_details)

        self.logger.info(
            json.dumps(
                {
                    "id": response.id,
                    "model": response.model,
                    "finish_reasons": [choice.finish_reason for choice in choices],
                    "messages_count": len(assistant_messages),
                    "tool_calls_count": sum(
                        len(message.tool_calls or [])
                        for message in assistant_messages
                    ),
                    "usage": {
                        "input": {
                            "text": input_details.text_tokens,
                            "image": input_details.image_tokens,
                            "audio": input_details.audio_tokens,
                            "video": input_details.video_tokens,
                            "cached": input_details.cached_tokens,
                            "total": usage.prompt_tokens,
                        },
                        "output": {
                            "text": output_details.text_tokens,
                            "image": output_details.image_tokens,
                            "audio": output_details.audio_tokens,
                            "video": output_details.video_tokens,
                            "reasoning": output_details.reasoning_tokens,
                            "total": usage.completion_tokens,
                        } if output_details is not None else {},
                        "total": usage.total_tokens,
                    }
                }
            )
        )

        return assistant_messages