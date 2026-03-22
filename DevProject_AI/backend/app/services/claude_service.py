# Low-level Claude API helpers.
# Handles client initialisation, extracting text from API responses, and safely parsing JSON output.

import json
from anthropic import Anthropic
from app.core.config import ANTHROPIC_API_KEY


def get_claude_client():
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY is not set in the environment.")
    return Anthropic(api_key=ANTHROPIC_API_KEY)


def extract_text_from_response(response) -> str:
    parts = []
    for block in response.content:
        if hasattr(block, "text"):
            parts.append(block.text)
    return "\n".join(parts).strip()


def safe_parse_plan_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1]).strip()
    return json.loads(text)
