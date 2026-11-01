import json

def parse_action(response: str) -> dict[str, str]:
    if not "```" in response:
        return json.loads(response)

    action = (
        response.split("```action")[1]
            .split("```")[0]
            .strip()
    )
    return json.loads(action)


def parse_python_code(llm_response: str):
    if not "```" in llm_response:
        return llm_response

    return (
        llm_response
        .split("```python")[1]
        .split("```")[0]
        .strip()
    )