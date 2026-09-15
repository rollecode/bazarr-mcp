"""Call real generated tools and check the requests they build.

The coverage tests read tools.py as text and the runtime tests exercise call()
directly, so without this nothing proves a generated function actually
produces the request its docstring claims.
"""

import json

import httpx
import pytest

from bazarr_mcp import runtime, tools


@pytest.fixture(autouse=True)
def transport(monkeypatch):
    monkeypatch.setenv("BAZARR_API_KEY", "k")
    monkeypatch.setenv("BAZARR_URL", "http://bazarr.test")
    runtime._http = None
    seen: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["method"] = request.method
        seen["path"] = request.url.path
        seen["query"] = dict(request.url.params)
        content_type = request.headers.get("content-type", "")
        if request.content and "json" in content_type:
            seen["body"] = json.loads(request.content)
            seen["form"] = {}
        elif request.content:
            from urllib.parse import parse_qs

            seen["body"] = None
            seen["form"] = {
                k: v[0] for k, v in parse_qs(request.content.decode()).items()
            }
        else:
            seen["body"] = None
            seen["form"] = {}
        return httpx.Response(200, json={"ok": True})

    runtime._http = httpx.Client(
        base_url="http://bazarr.test",
        headers={"X-API-KEY": "k"},
        transport=httpx.MockTransport(handler),
    )
    yield seen
    runtime._http = None


def test_a_collection_read_hits_the_collection(transport):
    result = json.loads(tools.list_episodes())
    assert result["status"] == "success"
    assert transport["method"] == "GET"
    assert transport["path"] == "/api/episodes"


def test_a_write_sends_its_form_fields(transport):
    tools.create_episodes_blacklist(
        seriesid=1,
        episodeid=2,
        provider="opensubtitles",
        subs_id="abc",
        language="fi",
        subtitles_path="/x.srt",
    )
    assert transport["method"] == "POST"
    assert transport["path"] == "/api/episodes/blacklist"
    # Bazarr reads form fields, not a JSON body.
    assert transport["body"] is None
    assert transport["form"]["provider"] == "opensubtitles"



def test_a_delete_reaches_the_right_path(transport):
    tools.delete_episodes_blacklist(all="false", provider="opensubtitles", subs_id="abc")
    assert transport["method"] == "DELETE"
    assert transport["path"] == "/api/episodes/blacklist"


def test_a_failure_comes_back_as_a_structured_error():
    runtime._http = httpx.Client(
        base_url="http://bazarr.test",
        transport=httpx.MockTransport(lambda request: httpx.Response(404)),
    )
    result = json.loads(tools.list_episodes())
    assert result["status"] == "error"


def test_annotations_match_what_each_tool_does():
    import asyncio

    registered = {t.name: t for t in asyncio.run(runtime.mcp.list_tools())}
    assert registered["list_episodes"].annotations.readOnlyHint is True
    assert registered["delete_episodes_blacklist"].annotations.destructiveHint is True
    assert registered["create_episodes_blacklist"].annotations.readOnlyHint is False
