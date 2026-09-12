#!/bin/sh
set -eu
project_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ ! -x "$project_dir/.venv/bin/python" ]; then
    echo 'Run sh Install.sh first.' >&2
    exit 1
fi
exec "$project_dir/.venv/bin/python" -m firestorm_mcp.probe "$@"
