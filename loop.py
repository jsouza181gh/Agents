import os
import json
from litellm import completion

def list_files():
    return {"results": os.listdir("informations")}


def read_file(file_name):
    with open(f"informations/{file_name}", encoding="utf-8") as file:
        try: 
            content = file.read()
            return {"result": content}

        except FileNotFoundError:
            return {"error": f"The file {file_name}, was not found."}

        except Exception as e:
            return {"error": f"The file {file_name}, could not be readed.\n{e}"}


def terminate(task):
    print(f"Resultado Final: {task}")


def get_tool_result(tool_name, args=None):
    match tool_name:
        case "list_files":
            return list_files()

        case "read_file":
            return read_file(args)

        case "terminate":
            return terminate(args)

        case _:
            return {"error": f"The tool {tool_name} is not avaliable."}


def call_llm(messages):
    response = completion(
        model="gemini/gemini-3.1-flash-lite",
        messages=messages
    )

    return response.choices[0].message.content.strip()


def parse_action_markdown(response):
    if not "```" in response:
        return response

    action = (
        response.split("```action")[1]
            .split("```")[0]
            .strip()
    )
    return json.loads(action)


def execute_agent_loop(system_prompt, memory, max_iterations):
    iteration = 1

    while iteration <= max_iterations:
        messages = system_prompt + memory
        print(f"\nStarting iteration {iteration}, calling LLM...\n")
        
        response = call_llm(messages)
        print(f"Response: {response}\n")

        action = parse_action_markdown(response)
        print(f"Selected Action: {action}\n")

        feedback = get_tool_result(action["tool_name"], action["args"])

        if action["tool_name"] == "terminate":
            break

        print(f"Tool Result: {feedback}")

        new_messages = [
            {
                "role": "assistant",
                "content": response
            },
            {
                "role": "user",
                "content": json.dumps(feedback)
            }
        ]

        memory.extend(new_messages)
        
        iteration += 1


def main():
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
    
    execute_agent_loop(
        system_prompt=system_prompt,
        memory=user_task,
        max_iterations=10
    )

if __name__ == "__main__":
    main()