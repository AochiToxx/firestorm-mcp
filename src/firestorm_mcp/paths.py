"""Machine-local state, independent of the checkout or wheel installation."""
import os
from pathlib import Path


def data_root():
    override = os.environ.get("FIRESTORM_MCP_HOME")
    if override:
        return Path(override).expanduser().resolve()
    if os.name == "nt":
        return Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local")) / "FirestormMCP"
    return Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state")) / "firestorm-mcp"


def viewer_directory():
    return Path(os.environ.get("FIRESTORM_VIEWER_DIR", r"C:\Program Files\Firestorm-Releasex64"))
