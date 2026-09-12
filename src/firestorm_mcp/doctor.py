"""Read-only setup diagnostics. Never contact a viewer or read session tokens."""
import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import platform

from . import __version__
from .paths import data_root, find_viewer, host_platform


def platform_support():
    return {"system": host_platform(), "architecture": platform.machine(),
            "native_file_dialogs": host_platform() == "win32",
            "file_selection": "Windows adapter (recognized dialogs only)" if host_platform() == "win32"
                              else "Manual selection in the viewer; native adapter unavailable"}


def diagnose(viewer=None, root=None):
    report = {"version": __version__, "python": platform.python_version(),
              "platform": platform_support(), "checks": [],
              "viewer_contacted": False, "viewer_started": False,
              "note": "Setup checks do not certify live viewer control. No private paths or tokens are included."}
    checks = report["checks"]
    packages = ["mcp", "llsd", "Pillow", "psutil", "jsonschema"]
    if host_platform() == "win32":
        packages.append("pywin32")
    for name in packages:
        try:
            checks.append({"check": name, "status": "ok", "version": importlib.metadata.version(name)})
        except importlib.metadata.PackageNotFoundError:
            checks.append({"check": name, "status": "missing", "fix": "Run the installer again in this environment"})
    try:
        find_viewer(viewer)
        checks.append({"check": "viewer_layout", "status": "ok"})
    except (OSError, ValueError):
        checks.append({"check": "viewer_layout", "status": "needs_attention",
                       "fix": "Install Firestorm and supply --viewer (exe/app/firestorm script); select one if multiple exist"})
    root = Path(root or data_root()).expanduser().resolve()
    parent = next((p for p in (root, *root.parents) if p.exists()), root)
    writable = parent.is_dir() and os.access(parent, os.W_OK)
    checks.append({"check": "state_location", "status": "ok" if writable else "needs_attention",
                   "note": "Permission precheck only; no files were written"})
    if host_platform().startswith("linux"):
        checks.append({"check": "graphical_session", "status": "detected" if
                       os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY") else "needs_attention",
                       "note": "Live Firestorm requires a graphical desktop; offline asset tools do not"})
    report["setup_ready"] = all(c["status"] in ("ok", "detected") for c in checks)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--viewer", type=Path)
    parser.add_argument("--data-dir", type=Path, default=data_root())
    args = parser.parse_args()
    try:
        report = diagnose(args.viewer, args.data_dir)
        print(json.dumps(report, indent=2))
        parser.exit(0 if report["setup_ready"] else 2)
    except OSError as exc:
        parser.exit(1, f"Setup diagnostics failed: {type(exc).__name__}; check directory permissions\n")


if __name__ == "__main__":
    main()
