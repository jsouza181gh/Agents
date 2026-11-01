import subprocess
import sys

from utils import parse_python_code
from llm_service import LLMService

llm = LLMService()

MEMORY: list[dict[str, str]] = []

def update_memory(content: str, role: str="user"):
    MEMORY.append({"role": role, "content": content})


system_prompt = "You are specialist in python programming, you must answer in a ```python code block```."

update_memory(system_prompt, "system")

user_prompt=input("O que você gostaria hoje?\n").strip()

update_memory(user_prompt)

response = llm.generate_response(MEMORY)

update_memory(response["result"], "assistant")

command = parse_python_code(response["result"])

print("\nCódigo gerado:\n")
print(command)

if input("\nExecutar este código? [s/N] ").strip().lower() != "s":
    print("Execução cancelada.")
    sys.exit(0)

try:
    resultado = subprocess.run(
        [sys.executable, "-c", command],
        capture_output=True,
        text=True,
        timeout=30
    )
except subprocess.TimeoutExpired:
    print("Execução interrompida: passou de 30 segundos.")
    sys.exit(1)

if resultado.stdout:
    print("Saída:", resultado.stdout)

if resultado.stderr:
    print("Erros:", resultado.stderr)
