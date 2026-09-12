"""Print local stdio configuration; never edit an MCP host or launch a viewer."""
import argparse
import json
import os
from pathlib import Path
import sys

from .paths import data_root, find_viewer


def configuration(root=None, viewer=None):
    root = Path(root or data_root()).expanduser().resolve()
    try:
        resources = find_viewer(viewer).resources
    except FileNotFoundError:
        if viewer or os.environ.get("FIRESTORM_VIEWER") or os.environ.get("FIRESTORM_VIEWER_DIR"):
            raise
        # Offline-first installs must not pin a nonexistent resource path into
        # configuration. Let the server discover a viewer installed later.
        resources = None
    # Do not resolve this symlink: POSIX venv Python often points at system Python.
    python = str(Path(sys.executable).absolute())
    arguments = ["-m", "firestorm_mcp.server", "--tool-profile", "compact", "--data-dir", str(root)]
    if resources is not None:
        arguments += ["--viewer-dir", str(resources)]
    return {"mcpServers": {"firestorm": {"command": python, "args": arguments}}}


def render(config, format="json"):
    entry = config["mcpServers"]["firestorm"]
    if format == "codex":
        # TOML accepts Unicode scalars, but rejects JSON's surrogate-pair escapes.
        return ("[mcp_servers.firestorm]\ncommand = " + json.dumps(entry["command"], ensure_ascii=False) +
                "\nargs = " + json.dumps(entry["args"], ensure_ascii=False) + "\ntool_timeout_sec = 180")
    if format == "vscode":
        return json.dumps({"servers": {"firestorm": {"type": "stdio", **entry}}}, indent=2)
    if format != "json":
        raise ValueError("Unknown configuration format")
    return json.dumps(config, indent=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--viewer", type=Path, help="Explicit installed viewer, including a macOS .app")
    parser.add_argument("--data-dir", type=Path, default=data_root())
    parser.add_argument("--format", choices=("json", "codex", "vscode"), default="json",
                        help="JSON mcpServers, Codex TOML, or VS Code servers; all preserve the same paths")
    args = parser.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        print(render(configuration(args.data_dir, args.viewer), args.format))
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Configuration failed: {exc}\n")


if __name__ == "__main__":
    main()
