# Low-level Claude API helpers.
# Handles client initialisation, extracting text from API responses, and safely parsing JSON output.

import json

from anthropic import Anthropic
from anthropic.types import Message

from app.core.config import ANTHROPIC_API_KEY

# Module-level singleton — avoids recreating the client on every request
_client: Anthropic | None = None


def get_claude_client() -> Anthropic:
    global _client
    if _client is None:
        _client = Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def extract_text_from_response(response: Message) -> str:
    parts = []
    for block in response.content:
        if hasattr(block, "text"):
            parts.append(block.text)
    return "\n".join(parts).strip()


def safe_parse_plan_json(text: str) -> dict:
    """
    Extract and parse JSON from Claude's response.
    Handles clean JSON, markdown-fenced JSON, and JSON embedded in surrounding prose.
    """
    text = text.strip()

    # Fast path — response is already plain JSON
    if text.startswith("{"):
        return json.loads(text)

    # Strip markdown fences if present (```json ... ``` or ``` ... ```)
    if "```" in text:
        start = text.find("```")
        end = text.rfind("```")
        if start != end:
            inner = text[start + 3:end].strip()
            # Remove optional language specifier (e.g. "json\n")
            if inner.startswith("json"):
                inner = inner[4:].strip()
            return json.loads(inner)

    # Fallback — extract content between first { and last }
    brace_start = text.find("{")
    brace_end = text.rfind("}")
    if brace_start != -1 and brace_end != -1:
        return json.loads(text[brace_start:brace_end + 1])

    raise ValueError("No JSON object found in response")
