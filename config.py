import os
from dotenv import load_dotenv
from typing import cast

load_dotenv()

required_fields = {
    "LLM_MODEL" : os.getenv("LLM_DEFAULT_MODEL"),
    "MAX_RETRIES" : os.getenv("MAX_RETRIES")
}

missing_fields = [
    field 
    for field, value in required_fields.items()
    if not value
]

if any(missing_fields):
    raise RuntimeError(f"Missing Fields: {", ".join(missing_fields)}.")

LLM_MODEL = cast(str, required_fields["LLM_MODEL"])
MAX_RETRIES = cast(int, required_fields["MAX_RETRIES"])
FALLBACK_MODEL = os.getenv("LLM_FALLBACK_MODEL")