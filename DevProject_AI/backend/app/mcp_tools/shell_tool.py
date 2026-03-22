import subprocess

from app.schemas.plan import MCPContext, MCPSourceType

MAX_OUTPUT_LENGTH = 10_000  # truncate at 10 KB
TIMEOUT_SECONDS = 10


def run_shell_context(command: str) -> MCPContext:
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
        output = result.stdout or result.stderr
        output = output.strip()[:MAX_OUTPUT_LENGTH]

        if not output:
            output = f"Command ran successfully but produced no output. Exit code: {result.returncode}"

    except subprocess.TimeoutExpired:
        raise ValueError(f"Command timed out after {TIMEOUT_SECONDS}s: '{command}'")
    except Exception as e:
        raise ValueError(f"Failed to run command '{command}': {e}")

    return MCPContext(
        source=command,
        source_type=MCPSourceType.tool,
        content=output,
    )
