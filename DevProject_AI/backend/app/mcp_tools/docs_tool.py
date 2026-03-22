from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError
from html.parser import HTMLParser

from app.schemas.plan import MCPContext, MCPSourceType

MAX_CONTENT_LENGTH = 10_000  # truncate at 10 KB


class _HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self._parts = []
        self._skip_tags = {"script", "style", "head"}
        self._current_skip = None

    def handle_starttag(self, tag, attrs):
        if tag in self._skip_tags:
            self._current_skip = tag

    def handle_endtag(self, tag):
        if tag == self._current_skip:
            self._current_skip = None

    def handle_data(self, data):
        if self._current_skip is None:
            text = data.strip()
            if text:
                self._parts.append(text)

    def get_text(self) -> str:
        return "\n".join(self._parts)


def _fetch_url(url: str) -> str:
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=10) as response:
            raw = response.read().decode("utf-8", errors="ignore")
        parser = _HTMLTextExtractor()
        parser.feed(raw)
        return parser.get_text()[:MAX_CONTENT_LENGTH]
    except URLError as e:
        raise ValueError(f"Failed to fetch URL '{url}': {e}")


def _read_file(path: str) -> str:
    file = Path(path).resolve()
    if not file.exists() or not file.is_file():
        raise ValueError(f"File not found: {path}")
    return file.read_text(encoding="utf-8", errors="ignore")[:MAX_CONTENT_LENGTH]


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
