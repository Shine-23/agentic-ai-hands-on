# MCP tool: Docs context.
# Fetches content from a URL (strips HTML to plain text) or reads a local file
# and returns it as an MCPContext object to pass to Claude.

from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError
from html.parser import HTMLParser

from app.schemas.plan import MCPContext, MCPSourceType

MAX_CONTENT_BYTES = 10_000   # stop reading after 10 KB
FETCH_TIMEOUT     = 10       # seconds before URL fetch times out


class _HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self._parts = []
        self._skip_tags = {"script", "style", "head"}
        self._skip_stack = []   # stack so nested skip tags work correctly

    def handle_starttag(self, tag, attrs):
        if tag in self._skip_tags:
            self._skip_stack.append(tag)

    def handle_endtag(self, tag):
        if self._skip_stack and tag == self._skip_stack[-1]:
            self._skip_stack.pop()

    def handle_data(self, data):
        if not self._skip_stack:
            text = data.strip()
            if text:
                self._parts.append(text)

    def get_text(self) -> str:
        return "\n".join(self._parts)


def _fetch_url(url: str) -> str:
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=FETCH_TIMEOUT) as response:
            # Read in chunks to avoid loading huge pages into memory
            chunks = []
            total = 0
            while total < MAX_CONTENT_BYTES:
                chunk = response.read(4096)
                if not chunk:
                    break
                chunks.append(chunk.decode("utf-8", errors="ignore"))
                total += len(chunk)
            raw = "".join(chunks)
    except URLError as e:
        raise ValueError(f"Failed to fetch URL '{url}': {e}")

    parser = _HTMLTextExtractor()
    parser.feed(raw)
    text = parser.get_text()

    if not text.strip():
        raise ValueError(f"No readable text extracted from '{url}'. The page may be JavaScript-rendered.")

    return text[:MAX_CONTENT_BYTES]


def _read_file(path: str) -> str:
    file = Path(path).resolve()
    if not file.exists() or not file.is_file():
        raise ValueError(f"File not found: {path}")

    # Read in chunks to avoid loading huge files into memory
    chunks = []
    total = 0
    with file.open(encoding="utf-8", errors="ignore") as f:
        while total < MAX_CONTENT_BYTES:
            chunk = f.read(4096)
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)

    content = "".join(chunks)
    if not content.strip():
        raise ValueError(f"File is empty: {path}")

    return content


def fetch_docs_context(source: str) -> MCPContext:
    if source.startswith("http://") or source.startswith("https://"):
        content = _fetch_url(source)
        source_type = MCPSourceType.url
    else:
        content = _read_file(source)
        source_type = MCPSourceType.docs

    return MCPContext(
        source=source,
        source_type=source_type,
        content=content,
    )
