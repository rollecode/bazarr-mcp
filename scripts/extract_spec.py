#!/usr/bin/env python3
"""Build an OpenAPI document from Bazarr's source.

Bazarr serves Swagger, but only from a running instance: flask_restx assembles
it at runtime from decorators. Reading those decorators statically gives the
same surface without needing a live Bazarr, and it can be re-run against any
tag to see what changed.

The shapes this reads:

    @api_ns_episodes.route('episodes')
    class Episodes(Resource):
        get_request_parser = reqparse.RequestParser()
        get_request_parser.add_argument('seriesid[]', type=int, help='...')

        def get(self):
            \"\"\"List episodes metadata\"\"\"

Each `def get/post/patch/delete` becomes an operation, and the matching
`<method>_request_parser` supplies its parameters.

    python scripts/extract_spec.py /path/to/bazarr/bazarr/api openapi.json
"""

import ast
import json
import pathlib
import sys

METHODS = ("get", "post", "patch", "delete", "put")

# Bazarr mounts every namespace under this prefix.
PREFIX = "/api/"

_TYPES = {
    "int": "integer",
    "float": "number",
    "str": "string",
    "bool": "boolean",
}


def route_of(node: ast.ClassDef) -> str | None:
    """The path a class is mounted at, from its @api_ns_*.route decorator."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call):
            continue
        func = decorator.func
        mounted = isinstance(func, ast.Attribute) and func.attr == "route"
        if mounted and decorator.args and isinstance(decorator.args[0], ast.Constant):
            return decorator.args[0].value
    return None


def parsers_of(node: ast.ClassDef) -> dict[str, list[dict]]:
    """Collect add_argument calls, keyed by the method their parser serves."""
    parsers: dict[str, list[dict]] = {}
    for statement in ast.walk(node):
        if not isinstance(statement, ast.Call):
            continue
        func = statement.func
        if not (isinstance(func, ast.Attribute) and func.attr == "add_argument"):
            continue
        if not isinstance(func.value, ast.Name):
            continue

        owner = func.value.id  # e.g. get_request_parser
        method = owner.split("_")[0]
        if method not in METHODS:
            continue
        if not statement.args or not isinstance(statement.args[0], ast.Constant):
            continue

        argument = {
            "name": statement.args[0].value,
            "type": "string",
            "required": False,
            "help": "",
            "action": None,
        }
        for keyword in statement.keywords:
            if keyword.arg == "type" and isinstance(keyword.value, ast.Name):
                argument["type"] = _TYPES.get(keyword.value.id, "string")
            elif keyword.arg == "required" and isinstance(keyword.value, ast.Constant):
                argument["required"] = bool(keyword.value.value)
            elif keyword.arg == "help" and isinstance(keyword.value, ast.Constant):
                argument["help"] = keyword.value.value
            elif keyword.arg == "action" and isinstance(keyword.value, ast.Constant):
                argument["action"] = keyword.value.value

        parsers.setdefault(method, []).append(argument)
    return parsers


def as_parameter(argument: dict, location: str) -> dict:
    schema: dict = {"type": argument["type"]}
    # action='append' means the argument may repeat, which is a list.
    if argument["action"] == "append":
        schema = {"type": "array", "items": {"type": argument["type"]}}
    return {
        "name": argument["name"],
        "in": location,
        "required": argument["required"],
        "description": argument["help"],
        "schema": schema,
    }


def summary_of(node: ast.FunctionDef, method: str, route: str) -> str:
    doc = ast.get_docstring(node)
    if doc:
        return doc.strip().splitlines()[0]
    return f"{method.upper()} {route}"


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2

    source = pathlib.Path(sys.argv[1])
    paths: dict[str, dict] = {}

    for file in sorted(source.rglob("*.py")):
        tree = ast.parse(file.read_text())
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            route = route_of(node)
            if route is None:
                continue

            parsers = parsers_of(node)
            path = PREFIX + route.lstrip("/")
            # flask converters like <string:pin_id> become OpenAPI templates.
            path = _normalise_converters(path)
            tag = file.parent.name if file.stem == "__init__" else file.stem

            for member in node.body:
                if not isinstance(member, ast.FunctionDef):
                    continue
                if member.name not in METHODS:
                    continue

                location = "query" if member.name == "get" else "formData"
                parameters = [
                    as_parameter(argument, location)
                    for argument in parsers.get(member.name, [])
                ]
                parameters.extend(_path_parameters(route))

                paths.setdefault(path, {})[member.name] = {
                    "summary": summary_of(member, member.name, route),
                    "tags": [tag],
                    "parameters": parameters,
                }

    spec = {
        "openapi": "3.0.2",
        "info": {
            "title": "Bazarr API",
            "version": "1.0.0",
            "description": "Extracted from Bazarr's flask_restx decorators.",
        },
        "paths": paths,
    }

    with open(sys.argv[2], "w") as handle:
        json.dump(spec, handle, indent=1)

    operations = sum(len(methods) for methods in paths.values())
    print(f"{len(paths)} paths, {operations} operations -> {sys.argv[2]}")
    return 0


def _normalise_converters(path: str) -> str:
    """Turn <string:pin_id> into {pin_id}, which the generator understands."""
    import re

    return re.sub(r"<(?:[a-z]+:)?([a-zA-Z_][a-zA-Z0-9_]*)>", r"{\1}", path)


def _path_parameters(route: str) -> list[dict]:
    import re

    found = []
    for converter, name in re.findall(
        r"<(?:([a-z]+):)?([a-zA-Z_][a-zA-Z0-9_]*)>", route
    ):
        found.append(
            {
                "name": name,
                "in": "path",
                "required": True,
                "description": "Path parameter.",
                "schema": {"type": _TYPES.get(converter or "str", "string")},
            }
        )
    return found


if __name__ == "__main__":
    raise SystemExit(main())
