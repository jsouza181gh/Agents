from dotenv import load_dotenv
from typing import cast
import os

load_dotenv()

required_fields = {
    "LLM_MODEL": os.getenv("LLM_DEFAULT_MODEL"),
    "MAX_RETRIES": os.getenv("MAX_RETRIES", 0),
    "MAX_TOKENS": os.getenv("MAX_RESPONSE_TOKENS", 0),
    "MAX_ITERATIONS": os.getenv("MAX_ITERATIONS", 0)
}

missing_fields = [
    field 
    for field, value in required_fields.items()
    if not value
]

if any(missing_fields):
    raise RuntimeError(f"Missing Fields: {', '.join(missing_fields)}.")

LLM_MODEL = cast(str, required_fields["LLM_MODEL"])
FALLBACK_MODEL = os.getenv("LLM_FALLBACK_MODEL")
FREE_TIER = os.getenv("FREE_TIER", "false").lower() in ("1", "true", "yes")
FREE_TIER_RPM = int(os.getenv("FREE_TIER_RPM") or 15)

MAX_TOKENS = int(required_fields["MAX_TOKENS"])
MAX_RETRIES = int(required_fields["MAX_RETRIES"])
MAX_ITERATIONS = int(required_fields["MAX_ITERATIONS"])