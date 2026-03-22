# MCP tool: Shell context.
# Runs a shell command and captures its output (e.g. pip list, cat requirements.txt)
# and returns it as an MCPContext object to pass to Claude.
#
# SECURITY NOTE: shell=True is required for compound commands (e.g. "pip list | head -20").
# A blocklist guards against obviously destructive patterns. Do not expose this
# endpoint publicly without additional access controls.

import subprocess

from app.schemas.plan import MCPContext, MCPSourceType

MAX_OUTPUT_LENGTH = 10_000  # truncate at 10 KB
TIMEOUT_SECONDS   = 10

# Patterns that are blocked regardless of intent
_BLOCKED_PATTERNS = [
    "rm -rf", "rm -f", "rmdir /s", "del /f",
    "format ", ":(){:|:&};:",  # fork bomb
    "shutdown", "reboot", "halt",
    "mkfs", "dd if=",
    "> /dev/", "wget ", "curl ",
]


def _is_blocked(command: str) -> bool:
    lowered = command.lower()
    return any(pattern in lowered for pattern in _BLOCKED_PATTERNS)


def run_shell_context(command: str) -> MCPContext:
    if not command or not command.strip():
        raise ValueError("Command must not be empty.")

    if _is_blocked(command):
        raise ValueError(f"Command blocked for safety reasons: '{command}'")

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )

        parts = []
        if result.stdout.strip():
            parts.append(result.stdout.strip())
        if result.stderr.strip():
            parts.append(f"[stderr]\n{result.stderr.strip()}")

        output = "\n".join(parts) if parts else "Command produced no output."

        if result.returncode != 0:
            output = f"[exit code {result.returncode}]\n{output}"

        output = output[:MAX_OUTPUT_LENGTH]

    except subprocess.TimeoutExpired:
        raise ValueError(f"Command timed out after {TIMEOUT_SECONDS}s: '{command}'")
    except OSError as e:
        raise ValueError(f"Failed to run command '{command}': {e}")

    return MCPContext(
        source=command,
        source_type=MCPSourceType.tool,
        content=output,
    )
