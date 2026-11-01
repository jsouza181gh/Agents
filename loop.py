from litellm import ModelResponse, Choices, Message, Usage#, CompletionTokensDetailsWrapper, PromptTokensDetailsWrapper
import logging

from llm_service import LLMService

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(message)s",
    handlers=[
        logging.FileHandler("logs/application.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.getLogger("LiteLLM").setLevel(logging.CRITICAL + 1)

def main():
    llm = LLMService()
    system_prompt =  [
        {
            "role": "system",
            "content": """
                You are a IA agent, you will make analisys to assist the user.
                You must return one of the tools to have more context and answer the user better.

                Avaliable tools:
                - list_files() -> list[str]: This will return the filenames; they contain all the information;
                - read_file(file_name: str) -> str: This will return the file's content, here is the information needly;
                - terminate(task: str): This finishes the loop, the argument task will be sent to user.

                You must respect the action format in response (JSON):
                ```action
                {
                   'tool_name': 'write here the tool name',
                   'args': 'write here the argument value'
                }
                ```
            """
        }
    ]

    user_task = [
        {
        "role": "user",
        "content": input("O que você quer para hoje?\n")
        }
    ]
    
    llm.execute_loop(
        system_prompt=system_prompt,
        memory=user_task,
        max_iterations=10
    )


if __name__ == "__main__":
    main()

ModelResponse(
    id='OwLmaqfoCpGgo_UP8cT38Aw',
    created=1793458746,
    model='gemini-3.1-flash-lite', 
    object='chat.completion', 
    system_fingerprint=None, 
    choices=[
        Choices(
            finish_reason='stop', 
            index=0, 
            message=Message(
                content='Oi! Tudo bem? Como posso te ajudar hoje?', 
                role='assistant', 
                tool_calls=None, 
                function_call=None, 
                images=[], 
                thinking_blocks=[], 
                provider_specific_fields={
                    'thought_signatures': [
                        'EnMKcQFpFH0TUWbpUoV7VnfbZGDBVOM8nlcgUhDBhN/il5ujqQD1ysLIvXuhUFdEQnxsdn6jwnsYP0He1AqCvJP2sn3ZATtinJDR/5Sg85MWDWV6D7mFY8E7N0Qc66yx51KfI6IT/UZlKrzKfx+w7Rgs7ynh'
                    ]
                }
            ), 
            provider_specific_fields={
                'native_finish_reason': 'STOP'
            }
        )
    ], 
    usage=Usage(
        completion_tokens=11, 
        prompt_tokens=3, 
        total_tokens=14, 
        # completion_tokens_details=CompletionTokensDetailsWrapper(
        #     accepted_prediction_tokens=None, 
        #     audio_tokens=None, 
        #     reasoning_tokens=None, 
        #     rejected_prediction_tokens=None, 
        #     text_tokens=11, 
        #     image_tokens=None, 
        #     video_tokens=None
        # ), 
        # prompt_tokens_details=PromptTokensDetailsWrapper(
        #     audio_tokens=None, 
        #     cached_tokens=None, 
        #     text_tokens=3, 
        #     image_tokens=None, 
        #     video_tokens=None
        # ), 
        cache_read_input_tokens=None
    ), 
    vertex_ai_grounding_metadata=[], 
    vertex_ai_url_context_metadata=[], 
    vertex_ai_safety_results=[], 
    vertex_ai_citation_metadata=[], 
    service_tier='default'
)