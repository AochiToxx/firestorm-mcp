"""Install into this extracted package's private environment on any Python OS."""
import argparse
from pathlib import Path
import subprocess
import sys
import venv


def install(project, development=False):
    if sys.version_info < (3, 11):
        raise RuntimeError("Python 3.11 or newer is required; select that Python and retry")
    environment = project / ".venv"
    python = environment / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    if environment.resolve() != environment.absolute() or (environment.exists() and
            (not (environment / "pyvenv.cfg").is_file() or not python.is_file())):
        raise RuntimeError(".venv is redirected, incomplete, or from another OS. Choose a fresh extraction folder")
    if not python.exists():
        venv.EnvBuilder(with_pip=True).create(environment)
    # All dependency changes stay inside this installation; never run global pip.
    subprocess.run([str(python), "-m", "pip", "--disable-pip-version-check",
                    "install", "--upgrade", "pip>=26.2,<27"], check=True)
    package = ["-e", ".[test]"] if development else [str(project)]
    subprocess.run([str(python), "-m", "pip", "--disable-pip-version-check", "install", *package],
                   cwd=project, check=True)
    return python


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--development", action="store_true")
    args = parser.parse_args()
    try:
        python = install(Path(__file__).resolve().parent, args.development)
        print("\nInstalled. Viewer and agent configuration have not been changed.", flush=True)
        print("MCP configuration: merge this entry into your host's local stdio settings:", flush=True)
        subprocess.run([str(python), "-m", "firestorm_mcp.configure"], check=True)
        print("\nWindows: Start-FirestormMCP.cmd / Check-FirestormMCP.cmd")
        print("Linux or macOS: sh Start-FirestormMCP.sh / sh Check-FirestormMCP.sh")
        print("Setup diagnostics: use this environment's Python -m firestorm_mcp.doctor")
        print("See docs/INSTALLATION.md for custom viewer paths, platform limits and host formats.")
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"Setup failed: {exc}\nOn Debian/Ubuntu, install python3-venv if venv/ensurepip is missing.\n")


if __name__ == "__main__":
    main()
