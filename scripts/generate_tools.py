#!/usr/bin/env python3
"""Generate one MCP tool per OpenAPI operation.

The Servarr apps publish a complete OpenAPI document and no operationIds, so
tool names are derived from the method and path. Running this writes
`tools.py`, which is committed: generated code that a reader can open and a
debugger can step through beats building signatures at import time.

    python scripts/generate_tools.py openapi.json src/sonarr_mcp/tools.py
"""

import builtins
import json
import keyword
import re
import sys
from collections import Counter

_RESERVED = set(dir(builtins)) | set(keyword.kwlist)

# Servarr paths all sit under a version prefix that adds nothing to a tool name.
_PREFIXES = ("/api/v3/", "/api/v1/", "/api/")

_VERB = {
    "get": "get",
    "post": "create",
    "put": "update",
    "delete": "delete",
    "patch": "patch",
}

_PY_TYPE = {
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "string": "str",
    "array": "list",
    "object": "dict",
}

_READ_METHODS = {"get"}
_DESTRUCTIVE_METHODS = {"delete"}

_HEADER = '''"""Generated from the OpenAPI document. Do not edit by hand.

Regenerate with:

    python scripts/generate_tools.py openapi.json {target}

One tool per operation, {count} of them, covering the whole API.
"""

from .runtime import _DESTRUCTIVE, _READ, _WRITE, call, mcp

'''


def strip_prefix(path: str) -> str:
    for prefix in _PREFIXES:
        if path.startswith(prefix):
            return path[len(prefix) :]
    return path.lstrip("/")


def tool_name(method: str, path: str) -> str:
    """Build a readable, deterministic name from the method and path."""
    rest = strip_prefix(path)
    segments = [s for s in rest.split("/") if s]

    words: list[str] = []
    for segment in segments:
        if segment.startswith("{"):
            name = segment.strip("{}")
            words.append("by_id" if name == "id" else f"by_{_snake(name)}")
            continue
        words.append(_snake(segment))

    verb = _VERB.get(method, method)
    # A GET that takes no path parameter reads a collection, which is a list.
    if method == "get" and not any(w.startswith("by_") for w in words):
        verb = "list"

    parts = [verb, *words]
    name = re.sub(r"_+", "_", "_".join(p for p in parts if p)).strip("_")

    # A bare "list" (from GET /) would shadow the builtin, and every generated
    # annotation below it that says `list` would then resolve to a function.
    if name in _RESERVED:
        name = f"{name}_root"
    return name


def _param(name: str) -> str:
    """A safe Python identifier for a parameter, keeping the wire name intact.

    Only keywords need escaping. A parameter may shadow a builtin freely --
    annotations are evaluated in the enclosing scope, where the name is not
    bound yet -- and `id` reads better to a caller than `id_`.
    """
    ident = _snake(name)
    if keyword.iskeyword(ident) or not ident.isidentifier():
        ident = f"{ident}_"
    return ident


def _snake(text: str) -> str:
    text = re.sub(r"[^0-9a-zA-Z]+", "_", text)
    text = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", text)
    return text.lower().strip("_")


def py_type(schema: dict | None) -> str:
    if not schema:
        return "str"
    if "$ref" in schema:
        return "dict"
    return _PY_TYPE.get(schema.get("type", "string"), "str")


def default_for(kind: str) -> str:
    return {"list": "None", "dict": "None"}.get(kind, "None")


def describe(operation: dict, method: str, path: str) -> str:
    summary = (operation.get("summary") or "").strip()
    if not summary:
        tags = operation.get("tags") or []
        subject = tags[0] if tags else strip_prefix(path).split("/")[0]
        summary = {
            "get": f"Read {subject}.",
            "post": f"Create {subject}.",
            "put": f"Update {subject}.",
            "delete": f"Delete {subject}.",
            "patch": f"Patch {subject}.",
        }.get(method, f"{method.upper()} {subject}.")
    if not summary.endswith("."):
        summary += "."
    return summary


def render(name: str, method: str, path: str, operation: dict) -> str:
    params = operation.get("parameters") or []
    path_params = [p for p in params if p.get("in") == "path"]
    query_params = [p for p in params if p.get("in") == "query"]
    # Some APIs take form fields rather than a JSON body; those become named
    # arguments too, sent form-encoded.
    form_params = [p for p in params if p.get("in") == "formData"]
    request_body = operation.get("requestBody")
    has_body = bool(request_body)
    # Most specs never set `required` on a request body, so the method
    # decides: you do not POST, PUT or PATCH nothing, while a DELETE that
    # declares a body almost never insists on one.
    body_required = bool((request_body or {}).get("required")) or method in (
        "post",
        "put",
        "patch",
    )

    # Python needs every parameter without a default ahead of those with one,
    # so required arguments are collected separately and joined first.
    required_args: list[str] = []
    args: list[str] = []
    doc_args: list[str] = []

    # A path parameter and a query parameter can share a name; the second one
    # to claim an identifier gets suffixed, and the wire name is unaffected.
    used: dict[str, str] = {}

    def claim(name: str, suffix: str) -> str:
        ident = _param(name)
        if ident in used.values():
            ident = f"{ident}_{suffix}"
        used[name + suffix] = ident
        return ident

    for param in path_params:
        kind = py_type(param.get("schema"))
        ident = claim(param["name"], "path")
        required_args.append(f"{ident}: {kind}")
        doc_args.append(
            f"        {ident}: {param.get('description') or 'Path parameter.'}"
        )

    if has_body:
        # A body the spec marks optional stays optional: a DELETE that takes
        # none must not demand one from the caller.
        if body_required:
            required_args.append("body: dict")
        else:
            args.append("body: dict | None = None")
        doc_args.append(
            "        body: Request payload. Read the matching GET or the "
            "/schema endpoint first to see the fields this resource expects."
        )

    form_idents: dict[str, str] = {}
    for param in form_params:
        kind = py_type(param.get("schema"))
        ident = claim(param["name"], "form")
        form_idents[param["name"]] = ident
        if param.get("required"):
            required_args.append(f"{ident}: {kind}")
        else:
            args.append(f"{ident}: {kind} | None = None")
        doc_args.append(
            f"        {ident}: {param.get('description') or 'Form field.'}"
        )

    query_idents: dict[str, str] = {}
    for param in query_params:
        kind = py_type(param.get("schema"))
        ident = claim(param["name"], "query")
        query_idents[param["name"]] = ident
        args.append(f"{ident}: {kind} | None = {default_for(kind)}")
        doc_args.append(
            f"        {ident}: {param.get('description') or 'Query parameter.'}"
        )

    if method in _READ_METHODS:
        annotation = "_READ"
    elif method in _DESTRUCTIVE_METHODS:
        annotation = "_DESTRUCTIVE"
    else:
        annotation = "_WRITE"

    url = path
    for param in path_params:
        url = url.replace(
            "{" + param["name"] + "}", "{" + used[param["name"] + "path"] + "}"
        )
    url_expr = f'f"{url}"' if path_params else f'"{url}"'

    query_expr = (
        "{"
        + ", ".join(f'"{p["name"]}": {query_idents[p["name"]]}' for p in query_params)
        + "}"
        if query_params
        else "None"
    )
    body_expr = "body" if has_body else "None"
    form_expr = (
        "{"
        + ", ".join(f'"{p["name"]}": {form_idents[p["name"]]}' for p in form_params)
        + "}"
        if form_params
        else "None"
    )

    signature = ", ".join(required_args + args)
    doc = describe(operation, method, path)

    lines = [f"@mcp.tool(annotations={annotation})", f"def {name}({signature}) -> str:"]
    lines.append(f'    """{doc}')
    lines.append("")
    lines.append(f"    {method.upper()} {path}")
    if doc_args:
        lines.append("")
        lines.append("    Args:")
        lines.extend(doc_args)
    lines.append('    """')
    lines.append(
        f'    return call("{method.upper()}", {url_expr}, '
        f"query={query_expr}, body={body_expr}, form={form_expr})"
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2

    with open(sys.argv[1]) as handle:
        spec = json.load(handle)
    target = sys.argv[2]

    operations: list[tuple[str, str, str, dict]] = []
    for path, methods in spec["paths"].items():
        for method, operation in methods.items():
            if method not in _VERB:
                continue
            operations.append((tool_name(method, path), method, path, operation))

    # Two operations can reduce to the same name (a collection and its schema
    # endpoint, say). Suffix the later ones rather than silently dropping one.
    counts = Counter(name for name, *_ in operations)
    seen: Counter = Counter()
    resolved = []
    for name, method, path, operation in operations:
        if counts[name] > 1:
            seen[name] += 1
            if seen[name] > 1:
                name = f"{name}_{seen[name]}"
        resolved.append((name, method, path, operation))

    body = "\n\n".join(
        render(name, method, path, operation)
        for name, method, path, operation in sorted(resolved)
    )
    with open(target, "w") as handle:
        handle.write(_HEADER.format(target=target, count=len(resolved)))
        handle.write(body)

    print(f"{len(resolved)} tools written to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
