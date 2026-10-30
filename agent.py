from litellm import completion
import subprocess

def generate_response(messages: list[dict]) -> str:
    """Call LLM to get response"""
    response = completion(
        model="gemini/gemini-3.1-flash-lite",
        messages=messages
    )
    return response.choices[0].message.content

MEMORY: list = []

def update_memory(content, role="user"):
    MEMORY.append({"role": role, "content": content})


def extract_python_code(llm_response: str):
    if not "```" in llm_response:
        return llm_response

    return (
        llm_response
        .split("```python")[1]
        .split("```")[0]
        .strip()
    )


system_prompt = "You are specialist in python programming, you must answer in a ```python code block```."

update_memory(system_prompt, "system")

user_prompt=input("O que você você gostaria hoje?\n").strip()

update_memory(user_prompt)

response = generate_response(MEMORY)

update_memory(response,"assistant")

command = extract_python_code(response)

resultado = subprocess.run(
    ["python", "-c", command],
    capture_output=True,
    text=True
)

if resultado.stderr:
    print("Erros:", resultado.stderr)