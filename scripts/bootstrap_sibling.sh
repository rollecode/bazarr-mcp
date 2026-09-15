#!/usr/bin/env bash
#
# Stamp out a sibling Servarr MCP server from this one.
#
#   scripts/bootstrap_sibling.sh radarr 7878 8443 /path/to/radarr-openapi.json
#
# Everything that differs between the Servarr apps is a name, a port, a logo
# and a spec. The generator, runtime and tests are identical, so they are
# copied rather than rewritten.

set -euo pipefail

APP=${1:?app name, lowercase}
APP_PORT=${2:?the app HTTP port}
MCP_PORT=${3:?port for this MCP server}
SPEC=${4:?path to openapi.json}

SRC=$(cd "$(dirname "$0")/.." && pwd)
DEST="$HOME/Projects/${APP}-mcp"
TITLE="$(tr '[:lower:]' '[:upper:]' <<<"${APP:0:1}")${APP:1}"

mkdir -p "$DEST/src/${APP}_mcp" "$DEST/scripts" "$DEST/tests" "$DEST/public"

cp "$SRC/scripts/generate_tools.py" "$DEST/scripts/"
cp "$SRC/scripts/bootstrap_sibling.sh" "$DEST/scripts/"
cp "$SRC/LICENSE" "$SRC/.gitignore" "$DEST/"
cp "$SPEC" "$DEST/openapi.json"

rewrite() { sed -e "s/sonarr/${APP}/g" -e "s/Sonarr/${TITLE}/g" -e "s/SONARR/$(tr '[:lower:]' '[:upper:]' <<<"$APP")/g" "$1"; }

rewrite "$SRC/src/sonarr_mcp/runtime.py" \
  | sed -e "s|http://127.0.0.1:8989|http://127.0.0.1:${APP_PORT}|" \
        -e "s/^DEFAULT_PORT = .*/DEFAULT_PORT = ${MCP_PORT}/" \
  > "$DEST/src/${APP}_mcp/runtime.py"
rewrite "$SRC/src/sonarr_mcp/__init__.py" > "$DEST/src/${APP}_mcp/__init__.py"
rewrite "$SRC/src/sonarr_mcp/server.py" > "$DEST/src/${APP}_mcp/server.py"
rewrite "$SRC/pyproject.toml" > "$DEST/pyproject.toml"
rewrite "$SRC/tests/test_coverage.py" > "$DEST/tests/test_coverage.py"
rewrite "$SRC/tests/test_runtime.py" > "$DEST/tests/test_runtime.py"

cd "$DEST"
python3 scripts/generate_tools.py openapi.json "src/${APP}_mcp/tools.py"

count=$(grep -c '^@mcp.tool' "src/${APP}_mcp/tools.py")
sed -i "s/    assert len(registered) == 234/    assert len(registered) == ${count}/" tests/test_runtime.py

echo "${DEST}: ${count} tools"
echo "still to do: instructions in runtime.py, logo in public/, README.md, CHANGELOG.md"
