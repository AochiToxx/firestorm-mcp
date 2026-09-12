"""Print local stdio configuration; never edit an MCP host or launch a viewer."""
import argparse
import json
from pathlib import Path
import sys

from .paths import data_root, find_viewer, viewer_directory


def configuration(root=None, viewer=None):
    root = Path(root or data_root()).expanduser().resolve()
    resources = find_viewer(viewer).resources if viewer else viewer_directory()
    # Do not resolve this symlink: POSIX venv Python often points at system Python.
    python = str(Path(sys.executable).absolute())
    return {"mcpServers": {"firestorm": {"command": python,
        "args": ["-m", "firestorm_mcp.server", "--tool-profile", "compact",
                 "--data-dir", str(root), "--viewer-dir", str(resources)]}}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--viewer", type=Path, help="Explicit installed viewer, including a macOS .app")
    parser.add_argument("--data-dir", type=Path, default=data_root())
    args = parser.parse_args()
    try:
        print(json.dumps(configuration(args.data_dir, args.viewer), indent=2))
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Configuration failed: {exc}\n")


if __name__ == "__main__":
    main()
