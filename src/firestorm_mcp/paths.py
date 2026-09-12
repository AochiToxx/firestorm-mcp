"""Machine-local state and viewer layouts, independent of the code installation."""
from dataclasses import dataclass
import os
from pathlib import Path
import plistlib
import shutil
import sys


def host_platform():
    return sys.platform


def data_root():
    override = os.environ.get("FIRESTORM_MCP_HOME")
    if override:
        return Path(override).expanduser().resolve()
    if host_platform() == "win32":
        return Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local")) / "FirestormMCP"
    if host_platform() == "darwin":
        return Path.home() / "Library/Application Support/FirestormMCP"
    xdg = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state"))
    if not xdg.is_absolute():
        xdg = Path.home() / ".local/state"
    return xdg / "firestorm-mcp"


@dataclass(frozen=True)
class ViewerInstallation:
    target: Path
    executable: Path
    resources: Path
    cwd: Path


def resolve_viewer(target: Path, system=None):
    """Validate an installed layout without starting or changing the viewer."""
    system = system or host_platform()
    target = target.expanduser().resolve(strict=True)
    if system == "darwin":
        if not target.is_dir() or target.suffix.lower() != ".app" or "firestorm" not in target.name.lower():
            raise ValueError("Select the installed Firestorm .app bundle with --viewer")
        with (target / "Contents/Info.plist").open("rb") as handle:
            name = plistlib.load(handle).get("CFBundleExecutable")
        if not isinstance(name, str) or not name or Path(name).name != name or name in (".", ".."):
            raise ValueError("The Firestorm bundle has no valid CFBundleExecutable")
        executable = (target / "Contents/MacOS" / name).resolve(strict=True)
        if not executable.is_relative_to(target):
            raise ValueError("The viewer executable must stay inside its .app bundle")
        resources = target / "Contents/Resources"
        cwd = resources
    elif system == "win32":
        if not target.is_file() or target.suffix.lower() != ".exe" or "firestorm" not in target.name.lower():
            raise ValueError("Select the installed Firestorm executable with --viewer")
        executable, resources, cwd = target, target.parent, target.parent
    elif system.startswith("linux"):
        # The distribution wrapper sets library/plugin paths. Never bypass it.
        if not target.is_file() or target.name != "firestorm":
            raise ValueError("Select the distribution's 'firestorm' launcher script, not its internal binary")
        executable, resources, cwd = target, target.parent, target.parent
    else:
        raise ValueError(f"Viewer launching is not implemented for {system}; offline MCP tools remain available")
    if not executable.is_file() or (system != "win32" and not os.access(executable, os.X_OK)):
        raise ValueError("The selected viewer is not executable; install it using Firestorm's instructions")
    if not (resources / "skins/default/xui/en/menu_viewer.xml").is_file():
        raise ValueError("Viewer resources are missing: skins/default/xui/en/menu_viewer.xml")
    return ViewerInstallation(target, executable, resources, cwd)


def viewer_candidates():
    """Search conventional locations only; never recursively scan a user's home."""
    system = host_platform()
    candidates = []
    if system == "win32":
        base = Path(os.environ.get("ProgramFiles", "C:/Program Files"))
        candidates += sorted(base.glob("*Firestorm*/*Firestorm*.exe"))
    elif system == "darwin":
        for base in (Path("/Applications"), Path.home() / "Applications"):
            candidates += sorted(base.glob("*Firestorm*.app"))
    elif system.startswith("linux"):
        on_path = shutil.which("firestorm")
        if on_path:
            candidates.append(Path(on_path))
        for base in (Path("/opt"), Path.home(), Path.home() / ".local/opt"):
            for pattern in ("*firestorm*/firestorm", "*Firestorm*/firestorm"):
                candidates += sorted(base.glob(pattern))
    return candidates


def find_viewer(target=None):
    explicit = target or os.environ.get("FIRESTORM_VIEWER")
    if explicit:
        return resolve_viewer(Path(explicit))
    directory = os.environ.get("FIRESTORM_VIEWER_DIR")
    if directory:
        base = Path(directory).expanduser()
        if host_platform() == "win32":
            candidates = sorted(base.glob("*Firestorm*.exe"))
        elif host_platform() == "darwin":
            candidates = [base.parent.parent if base.name == "Resources" else base]
        else:
            candidates = [base / "firestorm"]
    else:
        candidates = viewer_candidates()
    matches = {}
    for candidate in candidates:
        try:
            installed = resolve_viewer(candidate)
            matches[installed.target] = installed
        except (OSError, ValueError, plistlib.InvalidFileException):
            continue
    if len(matches) == 1:
        return next(iter(matches.values()))
    if len(matches) > 1:
        raise ValueError("Multiple Firestorm installations found; choose one with --viewer or FIRESTORM_VIEWER")
    raise FileNotFoundError("Firestorm was not found; install it, then supply --viewer or FIRESTORM_VIEWER")


def viewer_directory():
    override = os.environ.get("FIRESTORM_VIEWER_DIR")
    if override:
        base = Path(override).expanduser().resolve()
        return base / "Contents/Resources" if base.suffix.lower() == ".app" else base
    try:
        return find_viewer().resources
    except (OSError, ValueError):
        # Offline asset/protocol tools do not require an installed viewer.
        if host_platform() == "win32":
            return Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Firestorm-Releasex64"
        return data_root() / "viewer-not-configured"
