"""Server instance, client and the call helper every generated tool uses."""

import importlib.metadata
import json
import logging
import os

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.types import Icon

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

APP = "bazarr"
ENV_URL = "BAZARR_URL"
ENV_KEY = "BAZARR_API_KEY"
DEFAULT_URL = "http://127.0.0.1:6767"
DEFAULT_PORT = 8560

try:
    __version__ = importlib.metadata.version(f"{APP}-mcp")
except importlib.metadata.PackageNotFoundError:  # running from a source tree
    __version__ = "0.0.0"

_ICON_BASE = os.getenv("MCP_PUBLIC_URL", "").rstrip("/")
_ICON_SIZES = (48, 96, 256)

mcp = FastMCP(
    APP,
    icons=(
        [
            Icon(
                src=f"{_ICON_BASE}/icon.png"
                if size == 256
                else f"{_ICON_BASE}/icon-{size}.png",
                mimeType="image/png",
                sizes=[f"{size}x{size}"],
            )
            for size in _ICON_SIZES
        ]
        if _ICON_BASE
        else None
    ),
    website_url=_ICON_BASE or None,
    instructions=(
        "Manage a Bazarr instance: subtitles for the series and movies Sonarr "
        "and Radarr track. Search, download, upload, delete and blacklist "
        "subtitles, see what is wanted, read history, configure providers and "
        "language profiles, and run system tasks. Every API operation is a "
        "tool, named verb-first: list_* reads, create_* posts, update_* "
        "patches and delete_* removes. "
        "Start with list_episodes_wanted or list_movies_wanted to see what is "
        "missing, list_providers_episodes to see what is available for one "
        "episode, then update_episodes_subtitles to download it. Bazarr takes "
        "form fields rather than JSON bodies, which these tools handle."
    ),
)

mcp._mcp_server.version = __version__

_READ = {
    "readOnlyHint": True,
    "destructiveHint": False,
    "idempotentHint": True,
    "openWorldHint": False,
}
_WRITE = {
    "readOnlyHint": False,
    "destructiveHint": False,
    "idempotentHint": True,
    "openWorldHint": False,
}
_DESTRUCTIVE = {**_WRITE, "destructiveHint": True}

_http: httpx.Client | None = None


def _client() -> httpx.Client:
    global _http
    if _http is None:
        api_key = os.getenv(ENV_KEY)
        if not api_key:
            raise RuntimeError(
                f"{ENV_KEY} is not set. Find it in {APP.title()} under "
                "Settings, General, Security, API key."
            )
        _http = httpx.Client(
            base_url=(os.getenv(ENV_URL) or DEFAULT_URL).rstrip("/"),
            headers={"X-API-KEY": api_key},
            # A full library listing over a remote proxy genuinely
            # takes minutes; 60s times out on a few hundred items.
            timeout=httpx.Timeout(300.0, connect=15.0),
        )
    return _http


def _err(e: Exception) -> str:
    if isinstance(e, httpx.HTTPStatusError):
        status = e.response.status_code
        if status == 401:
            msg = f"{APP.title()} rejected the API key. Check {ENV_KEY}."
        elif status == 404:
            msg = "No such resource. Check the id."
        elif status == 400:
            # Servarr returns a validation array that says exactly which field
            # is wrong, which is far more useful than the status alone.
            msg = f"{APP.title()} rejected the request: {_detail(e.response)}"
        else:
            msg = f"{APP.title()} API error (HTTP {status}): {_detail(e.response)}"
    elif isinstance(e, httpx.ConnectError):
        msg = (
            f"Could not connect to {APP.title()}. Check that it is running and "
            f"{ENV_URL} points at it."
        )
    elif isinstance(e, httpx.TimeoutException):
        msg = f"Request timed out. {APP.title()} may be busy -- try again."
    else:
        msg = f"{type(e).__name__}: {e}"

    return json.dumps({"status": "error", "message": msg})


def _detail(response: httpx.Response) -> str:
    try:
        return json.dumps(response.json())[:800]
    except ValueError:
        return response.text[:400]


def call(
    method: str,
    path: str,
    query: dict | None = None,
    body: dict | None = None,
    form: dict | None = None,
) -> str:
    """Perform one API call and return its result as a JSON string."""
    try:
        params = {k: v for k, v in (query or {}).items() if v is not None}
        fields = {k: v for k, v in (form or {}).items() if v is not None}
        response = _client().request(
            method,
            path,
            params=params or None,
            json=body,
            data=fields or None,
        )
        response.raise_for_status()

        if not response.content:
            return json.dumps({"status": "success", "result": None})
        try:
            return json.dumps(
                {"status": "success", "result": response.json()}, indent=2
            )
        except ValueError:
            return json.dumps({"status": "success", "result": response.text})
    except Exception as e:
        return _err(e)


def main() -> None:
    import argparse

    from dotenv import find_dotenv, load_dotenv

    from . import tools  # noqa: F401 -- importing registers every tool

    dotenv_path = find_dotenv(usecwd=True)
    if dotenv_path and load_dotenv(dotenv_path, override=False):
        logger.info("Loaded .env from %s", dotenv_path)

    parser = argparse.ArgumentParser(prog=f"{APP}-mcp")
    parser.add_argument(
        "--transport",
        choices=("stdio", "http"),
        default=os.getenv("MCP_TRANSPORT", "stdio"),
    )
    parser.add_argument("--host", default=os.getenv("MCP_HOST", "127.0.0.1"))
    parser.add_argument(
        "--port", type=int, default=int(os.getenv("MCP_PORT", str(DEFAULT_PORT)))
    )
    args = parser.parse_args()

    if args.transport == "stdio":
        mcp.run(transport="stdio")
        return

    if args.host not in ("127.0.0.1", "::1", "localhost"):
        raise SystemExit(
            f"refusing to listen on {args.host}: this server has no login of "
            "its own. Keep it on the local machine and put a proxy in front."
        )

    mcp.settings.host = args.host
    mcp.settings.port = args.port
    logger.info("Listening on http://%s:%d/mcp", args.host, args.port)
    mcp.run(transport="streamable-http")
