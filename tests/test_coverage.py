"""Every operation in the OpenAPI document must be reachable from a tool.

Regenerating tools.py from a newer spec and running this is the whole upgrade
process: a new endpoint either appears as a tool or fails here.
"""

import ast
import json
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
SPEC = ROOT / "openapi.json"
TOOLS = ROOT / "src" / "bazarr_mcp" / "tools.py"

# HEAD duplicates a GET on the same path and carries no body, so it is not
# generated as a tool of its own.
IGNORED_METHODS = {"head", "options", "trace", "parameters"}


def spec_operations() -> set[tuple[str, str]]:
    spec = json.loads(SPEC.read_text())
    return {
        (method.upper(), path)
        for path, methods in spec["paths"].items()
        for method in methods
        if method not in IGNORED_METHODS
    }


def generated_calls() -> set[tuple[str, str]]:
    """Read back the method and path literal each generated tool calls."""
    tree = ast.parse(TOOLS.read_text())
    found = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not (isinstance(node.func, ast.Name) and node.func.id == "call"):
            continue
        method_node, path_node = node.args[0], node.args[1]
        if isinstance(path_node, ast.JoinedStr):
            path = "".join(
                part.value
                if isinstance(part, ast.Constant)
                else "{" + ast.unparse(part.value) + "}"
                for part in path_node.values
            )
        else:
            path = path_node.value
        found.add((method_node.value, path))
    return found


def normalise(pairs: set[tuple[str, str]]) -> set[tuple[str, str]]:
    """Path parameter names are snake_cased in the generated f-strings."""
    import re

    def clean(path: str) -> str:
        return re.sub(r"\{[^}]+\}", "{}", path)

    return {(method, clean(path)) for method, path in pairs}


def test_every_operation_has_a_tool():
    missing = normalise(spec_operations()) - normalise(generated_calls())
    assert not missing, f"{len(missing)} operations have no tool: {sorted(missing)[:10]}"


def test_no_tool_calls_an_endpoint_outside_the_spec():
    extra = normalise(generated_calls()) - normalise(spec_operations())
    assert not extra, f"tools call endpoints the spec does not define: {sorted(extra)}"


def test_tool_names_are_unique():
    tree = ast.parse(TOOLS.read_text())
    names = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
    duplicates = {n for n in names if names.count(n) > 1}
    assert not duplicates, f"duplicate tool names: {duplicates}"


def test_each_method_in_the_spec_is_represented():
    assert {m for m, _ in spec_operations()} == {m for m, _ in generated_calls()}


def test_generated_and_spec_agree_exactly():
    assert normalise(generated_calls()) == normalise(spec_operations())
