from litellm import completion, ModelResponse
from dataclasses import dataclass
from typing import cast
import logging
import json

from config import LLM_MODEL, FALLBACK_MODEL, MAX_RETRIES
from tools import list_files, read_file, terminate, ToolResult
from utils import parse_action

@dataclass
class LLMService:
    model: str = LLM_MODEL
    retries: int = MAX_RETRIES
    fallback_models: str | None = FALLBACK_MODEL
    logger = logging.getLogger(__name__)

    def generate_response(self, messages: list[dict[str, str]]) -> dict[str, str]:
        response = cast(
            ModelResponse,
            completion(
                model=self.model,
                messages=messages,
                num_retries=self.retries
            )
        )

        content = response.choices[0].message.content

        if content is None:
            self.logger.warning("The LLM returned an empty response")
            return {"error": "The LLM returned an empty response."}

        return {"result": content.strip()}


    def execute_loop(self, system_prompt: list[dict[str, str]], memory: list[dict[str, str]], max_iterations: int):
        iteration = 1
    
        while iteration <= max_iterations:
            messages = system_prompt + memory
            self.logger.info(f"Executing loop, iteration {iteration}")
            
            response = self.generate_response(messages=messages)
            self.logger.info(f"Response: {response}")
    
            if response.get("error"):
                self.logger.error(response["error"])
                break
    
            action = parse_action(response["result"])
            self.logger.info(f"Selected Action: {action}")
    
            feedback = self.get_tool_result(action["tool_name"], action["args"])
    
            if action["tool_name"] == "terminate":
                self.logger.info(feedback)
                return feedback
    
            self.logger.info(f"Tool Result: {feedback}")
    
            new_messages = [
                {
                    "role": "assistant",
                    "content": response["result"]
                },
                {
                    "role": "user",
                    "content": json.dumps(feedback)
                }
            ]
    
            memory.extend(new_messages)
            
            iteration += 1


    def get_tool_result(self, tool_name: str, args: str | None = None) -> ToolResult:    
        match tool_name:
            case "list_files":
                return list_files()

            case "read_file":
                if args is None:
                    return {"error": f"The argument 'file_name' is not present in this tool call."}
                
                return read_file(args)

            case "terminate":
                if args is None:
                    return {"error": f"The argument 'message' is not present in this tool call."}
                
                return terminate(args)

            case _:
                return {"error": f"The tool {tool_name} is not avaliable."}