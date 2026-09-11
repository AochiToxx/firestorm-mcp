"""Opt-in Windows viewer launcher. Never closes or replaces a running viewer."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

from .paths import data_root, viewer_directory


def running_viewers():
    import psutil
    result = []
    for process in psutil.process_iter(["pid", "name", "exe"], ad_value=None):
        try:
            if "firestorm" in (process.info["name"] or "").lower():
                result.append({"pid": process.info["pid"], "name": process.info["name"]})
        except psutil.NoSuchProcess:
            continue
    return result


def session_settings(python, helper, runtime, viewer_dir):
    # LLProcess treats backslashes as escapes. Quote forward-slash paths.
    values = [str(p).replace("\\", "/") for p in (python, helper, runtime, viewer_dir)]
    if any('"' in value or "\n" in value or "\r" in value for value in values):
        raise ValueError("Paths must not contain quotes or newlines")
    command = f'"{values[0]}" "{values[1]}" --runtime "{values[2]}" --viewer-dir "{values[3]}"'
    root = ET.Element("llsd")
    settings = ET.SubElement(root, "map")
    ET.SubElement(settings, "key").text = "LeapCommand"
    value = ET.SubElement(settings, "map")
    ET.SubElement(value, "key").text = "Type"
    ET.SubElement(value, "string").text = "LLSD"
    ET.SubElement(value, "key").text = "Value"
    ET.SubElement(ET.SubElement(value, "array"), "string").text = command
    return ET.tostring(root, encoding="unicode")


def launch(viewer: Path, root: Path, login_screen=False, dry_run=False):
    if os.name != "nt":
        raise RuntimeError("The packaged viewer launcher currently supports Windows only")
    viewer = viewer.resolve(strict=True)
    if not viewer.is_file() or viewer.suffix.lower() != ".exe" or "firestorm" not in viewer.name.lower():
        raise ValueError("Select the installed Firestorm executable")
    active = running_viewers()
    if active:
        raise RuntimeError("Firestorm is already running. No process was changed; coordinate a later launcher start.")
    runtime = root.resolve() / "runtime"
    helper = Path(__file__).with_name("leap_entry.py").resolve(strict=True)
    settings = runtime / "session-settings.xml"
    xml = session_settings(Path(sys.executable), helper, runtime, viewer.parent)
    args = [str(viewer), "--sessionsettings", str(settings)]
    if login_screen:
        args.extend(["--set", "AutoLogin", "false"])
    if dry_run:
        return {"status": "dry_run", "viewer_started": False, "arguments": args, "helper": str(helper)}
    runtime.mkdir(parents=True, exist_ok=True)
    # A creation lock prevents simultaneous launches by cooperating clients.
    lock = runtime / "launch.lock"
    with lock.open("x", encoding="utf-8") as handle:
        handle.write(str(os.getpid()))
    try:
        if running_viewers():
            raise RuntimeError("Firestorm started during preparation; no second process was launched")
        settings.write_text(xml, encoding="utf-8")
        # This is the viewer UI explicitly requested by the caller, not a hidden helper.
        process = subprocess.Popen(args, cwd=viewer.parent)
        return {"status": "process_started", "pid": process.pid, "viewer_started": True,
                "bridge_connection_verified": False, "note": "Run firestorm-mcp-check to verify LEAP; sign in in the viewer."}
    finally:
        lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--viewer", type=Path, default=viewer_directory() / "Firestorm-Releasex64.exe")
    parser.add_argument("--data-dir", type=Path, default=data_root())
    parser.add_argument("--login-screen", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(launch(args.viewer, args.data_dir, args.login_screen, args.dry_run), indent=2))
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"{type(exc).__name__}: {exc}\n")


if __name__ == "__main__":
    main()
