from pathlib import Path
from typing import List, Optional

from app.schemas.plan import MCPContext, MCPSourceType

DEFAULT_EXTENSIONS = {".py", ".md", ".txt", ".json", ".yaml", ".yml", ".toml"}
MAX_FILE_SIZE_BYTES = 10_000  # skip files larger than 10 KB


def read_repo_context(
    directory: str,
    extensions: Optional[List[str]] = None,
    max_files: int = 20,
) -> List[MCPContext]:
    root = Path(directory).resolve()

    if not root.exists() or not root.is_dir():
        raise ValueError(f"Directory not found: {directory}")

    allowed = set(extensions) if extensions else DEFAULT_EXTENSIONS
    contexts = []

    for path in sorted(root.rglob("*")):
        if len(contexts) >= max_files:
            break
        if not path.is_file():
            continue
        if path.suffix not in allowed:
            continue
        if path.stat().st_size > MAX_FILE_SIZE_BYTES:
            continue

        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
            relative = str(path.relative_to(root))
            contexts.append(
                MCPContext(
                    source=relative,
                    source_type=MCPSourceType.repo,
                    content=content,
                )
            )
        except Exception:
            continue

    return contexts
