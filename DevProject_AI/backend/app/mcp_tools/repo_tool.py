# MCP tool: Repo context.
# Scans a local directory or clones a public GitHub repo (supports tree/subdir URLs)
# and returns file contents as MCPContext objects to pass to Claude.

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional

from app.schemas.plan import MCPContext, MCPSourceType

DEFAULT_EXTENSIONS = {".py", ".md", ".txt", ".json", ".yaml", ".yml", ".toml"}
MAX_FILE_SIZE_BYTES = 10_000   # skip files larger than 10 KB
CLONE_TIMEOUT_SECONDS = 60

# Directories that are never useful as planning context
SKIP_DIRS = {
    ".git", ".github", ".venv", "venv", "env",
    "node_modules", "__pycache__", ".mypy_cache", ".pytest_cache",
    "dist", "build", ".eggs", "*.egg-info",
}


def _is_github_url(directory: str) -> bool:
    return directory.startswith("https://github.com") or directory.startswith("http://github.com")


def _parse_github_url(url: str) -> tuple[str, str]:
    """
    Returns (clone_url, subpath).
    Handles both repo root URLs and tree/subdirectory URLs:
      https://github.com/user/repo              -> clone_url=same, subpath=""
      https://github.com/user/repo/tree/main/src -> clone_url=https://github.com/user/repo, subpath="src"
    """
    url = url.rstrip("/")
    if "/tree/" in url:
        repo_part, rest = url.split("/tree/", 1)
        # rest is "{branch}/{subpath...}" or just "{branch}"
        parts = rest.split("/", 1)
        subpath = parts[1] if len(parts) > 1 else ""
        return repo_part, subpath
    return url, ""


def _clone_github_repo(clone_url: str) -> Path:
    # Use a parent temp dir and let git create the 'repo' subdirectory itself.
    # Cloning into a pre-existing directory can fail on some git/Windows versions.
    tmp_parent = tempfile.mkdtemp(prefix="devproject_repo_")
    clone_target = Path(tmp_parent) / "repo"
    try:
        result = subprocess.run(
            ["git", "clone", "--depth=1", clone_url, str(clone_target)],
            capture_output=True,
            text=True,
            timeout=CLONE_TIMEOUT_SECONDS,
        )
        if result.returncode != 0:
            shutil.rmtree(tmp_parent, ignore_errors=True)
            raise ValueError(f"git clone failed: {result.stderr.strip()}")
    except subprocess.TimeoutExpired:
        shutil.rmtree(tmp_parent, ignore_errors=True)
        raise ValueError(f"git clone timed out after {CLONE_TIMEOUT_SECONDS}s: '{clone_url}'")
    except FileNotFoundError:
        shutil.rmtree(tmp_parent, ignore_errors=True)
        raise ValueError("git is not installed or not on PATH")
    return clone_target


def _scan_directory(root: Path, extensions: Optional[List[str]], max_files: int) -> List[MCPContext]:
    allowed = set(extensions) if extensions else DEFAULT_EXTENSIONS
    contexts = []

    # Walk the generator directly — avoid materialising the full file list for large repos
    for path in root.rglob("*"):
        if len(contexts) >= max_files:
            break
        if not path.is_file():
            continue

        # Get path relative to root for skip-dir check
        try:
            relative_parts = path.relative_to(root).parts
        except ValueError:
            continue

        if any(part in SKIP_DIRS for part in relative_parts):
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
        except OSError as e:
            print(f"Skipping {path}: {e}")
            continue

    if not contexts:
        raise ValueError(
            "No readable files found. Check that the directory contains "
            f"files with extensions: {', '.join(sorted(allowed))}"
        )

    return contexts


def read_repo_context(
    directory: str,
    extensions: Optional[List[str]] = None,
    max_files: int = 20,
) -> List[MCPContext]:
    if _is_github_url(directory):
        clone_url, subpath = _parse_github_url(directory)
        clone_path = _clone_github_repo(clone_url)
        tmp_parent = clone_path.parent  # the temp dir wrapping the clone
        try:
            scan_root = clone_path / subpath if subpath else clone_path
            if not scan_root.exists() or not scan_root.is_dir():
                raise ValueError(f"Subpath '{subpath}' not found in cloned repo")
            return _scan_directory(scan_root, extensions, max_files)
        finally:
            shutil.rmtree(tmp_parent, ignore_errors=True)

    root = Path(directory).resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Directory not found: {directory}")

    return _scan_directory(root, extensions, max_files)
