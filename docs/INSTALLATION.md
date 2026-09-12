# Installation and configuration

## One setup procedure, local to your system

Download the `0.3.0a2` setup/source ZIP from [Releases](https://github.com/AochiToxx/firestorm-mcp/releases/tag/v0.3.0a2). Extract it to a permanent user-writable directory. Install Python 3.11–3.14 separately; install Firestorm separately if you need live viewer control. Internet access to your configured Python package index is required for installation. No root/admin shell is required.

| Action, from the extracted directory | Windows | Linux / macOS |
| --- | --- | --- |
| Install | `Install.cmd` or `python install.py` | `sh Install.sh` or `python3 install.py` |
| Print local MCP config again | `.venv\Scripts\python.exe -m firestorm_mcp.configure` | `.venv/bin/python -m firestorm_mcp.configure` |
| Check setup without a viewer connection | `.venv\Scripts\python.exe -m firestorm_mcp.doctor` | `.venv/bin/python -m firestorm_mcp.doctor` |
| Start the viewer when ready | `Start-FirestormMCP.cmd` | `sh Start-FirestormMCP.sh` |
| Check the existing connection | `Check-FirestormMCP.cmd` | `sh Check-FirestormMCP.sh` |

The common Python installer creates `.venv`, upgrades only that environment's pip and installs the package. It prints ready-to-copy JSON; it never edits agent configuration or starts Firestorm. `Install.cmd` keeps its console open until you press a key so a double-click launch does not lose the output. For unattended setup, invoke `python install.py` directly. Merge its `firestorm` entry into your host's configuration, keeping other servers. Host-specific wrappers are below. `--development` requests an editable installation with test dependencies.

Use `Install.ps1 -Python 'C:\path\to\python.exe' -Development` to select a Windows interpreter with the compatibility wrapper. On POSIX use `PYTHON=/absolute/path/to/python3 sh Install.sh`. Do not copy `.venv` between machines, rename a folder containing it, or install on top of an active consumer environment. Extract a fresh folder if the installer reports a redirected, incomplete or foreign-OS environment.

On Debian/Ubuntu and Raspberry Pi OS, a missing `venv`/`ensurepip` usually requires your OS's `python3-venv` package. If dependency installation attempts native compilation, consult [the platform notes](PLATFORMS.md); a Python wheel's `any` tag does not guarantee that every dependency supplies wheels for that OS/CPU. Do not use `sudo pip` or bypass the OS-managed Python protections.

The launch scripts remain unsigned. Follow local code execution and macOS Gatekeeper policy; review the downloaded source. You can use the documented Python modules directly without a PowerShell wrapper. `requirements-lock.txt` is the historical Windows/Python 3.12 development snapshot, not a portable install lockfile; the installer uses `pyproject.toml` and its platform markers.

## Select a nonstandard viewer location

The launcher detects conventional Windows Program Files, macOS Applications and Linux PATH/installation locations. If none or several are found, choose the exact viewer. The configuration generator and launcher accept the same `--viewer` option:

```sh
# Linux: use the distribution wrapper, never bin/do-not-directly-run-firestorm-bin.
.venv/bin/python -m firestorm_mcp.configure --viewer /opt/firestorm/firestorm
sh Start-FirestormMCP.sh --viewer /opt/firestorm/firestorm
```

```sh
# macOS: the bundle executable and Contents/Resources are derived from the .app.
.venv/bin/python -m firestorm_mcp.configure --viewer /Applications/Firestorm-Releasex64.app
sh Start-FirestormMCP.sh --viewer /Applications/Firestorm-Releasex64.app
```

```powershell
# Windows: use your actual executable name and location.
.\.venv\Scripts\python.exe -m firestorm_mcp.configure --viewer 'D:/Apps/Firestorm/Firestorm-Releasex64.exe'
.\Start-FirestormMCP.ps1 -Viewer 'D:/Apps/Firestorm/Firestorm-Releasex64.exe'
```

Regenerate/merge the printed config after selecting another viewer. Quoted `~` paths are expanded consistently by all Python entry points. Add matching `--data-dir` options to configure/launch/check if you choose a different state directory (`-DataDir` in the PowerShell wrapper). `FIRESTORM_VIEWER` is an environment alternative to `--viewer`; GUI hosts do not necessarily inherit shell exports, which is why generated config uses explicit resource/state paths.

The launcher validates the layout, leaves a running viewer alone and refuses an existing launch lock. `--dry-run` validates without launching/writing; `--login-screen` requests the login screen while normal launches retain the viewer's login preference. The Windows PowerShell equivalents are `-DryRun` and `-LoginScreen`. LEAP must start with the viewer; starting the MCP alone cannot attach to an existing normal viewer session.

## Generate the right format for your MCP host

Use the generator from the installed environment. It preserves **every** selected
argument, including `--data-dir` and `--viewer-dir`, in each host's wrapper. Do not
reconstruct a shorter command from an unrelated example or discard custom paths.

| Host | Generator option | Where the printed entry belongs |
| --- | --- | --- |
| Claude Desktop / Cursor and hosts using `mcpServers` | `--format json` (default) | The host's local MCP JSON; merge the `firestorm` entry |
| Codex | `--format codex` | The intended `config.toml` scope; merge `[mcp_servers.firestorm]` |
| VS Code extension host / Copilot | `--format vscode` | `.vscode/mcp.json`; merge the printed `servers.firestorm` entry |
| Claude Code and other CLI-configured hosts | Default JSON gives the exact command/args | Use the host's local stdio registration with the **entire** generated argument list |

Windows, from the extracted folder:

```powershell
.\.venv\Scripts\python.exe -m firestorm_mcp.configure --format codex
```

Linux/macOS, from the extracted folder:

```sh
.venv/bin/python -m firestorm_mcp.configure --format codex
```

Change `codex` to `json` or `vscode` for your host. Add the same `--viewer` and
`--data-dir` selections used for launch if they are nonstandard. The generated
command is absolute and retains the virtual environment; it does not depend on
the desktop app inheriting your terminal's PATH. If Firestorm has not been
installed yet, the default configuration leaves viewer discovery enabled instead
of pinning a nonexistent directory. Multiple detected viewers require a choice.

Codex output also sets `tool_timeout_sec = 180`, allowing longer multi-read
workflows than its default 60 seconds. It does not increase individual viewer RPC
timeouts or cancel an already-sent action. The generator changes no host files or
permissions. Follow [official Codex MCP configuration](https://developers.openai.com/codex/mcp).

These are format-checked examples, not a tested application UI matrix. Consult
[Cursor](https://cursor.com/docs/mcp), [Claude Code](https://code.claude.com/docs/en/mcp),
[local MCP servers](https://modelcontextprotocol.io/docs/develop/connect-local-servers)
or the [VS Code MCP reference](https://code.visualstudio.com/docs/agents/reference/mcp-configuration)
for the correct installation scope. VS Code's separate Agent Host can use another
scope; the `vscode` output targets the extension-host `servers` format. Keep the
compact profile when your host has tool-count limits; it changes discovery
presentation, not tool authority.

### Local desktop requirement

Run the server beside the viewer in the same desktop user session. The MCP host must support starting a local stdio process. A headless Pi, cloud-only agent, WSL or container does not gain access to another computer's desktop by installing this package. Remote MCP transport is not implemented. The helper's private `/rpc` URL is internal authenticated IPC, not an MCP HTTP endpoint; do not put it in the host's `url` setting or publish/tunnel it.

## Paths and machine-local state

| OS | Default state/captures | Viewer resources |
| --- | --- | --- |
| Windows | `%LOCALAPPDATA%\FirestormMCP` | Selected executable's containing folder |
| macOS | `~/Library/Application Support/FirestormMCP` | Selected `.app/Contents/Resources` |
| Linux | `${XDG_STATE_HOME:-~/.local/state}/firestorm-mcp` | Selected distribution wrapper's containing folder |

Use `FIRESTORM_MCP_HOME` or matching `--data-dir` options to override state. Use the generated configuration for nonstandard installations; it sets `--viewer-dir` to the selected resources. `FIRESTORM_VIEWER_DIR` remains an explicit resource-directory override. Never point it at a different viewer's skin definitions. `--root` remains a server/probe alias for `--data-dir`.

The state directory includes `runtime/connection.json` (a private session token), session settings and captures. Keep it local and out of cloud sync or source repositories. POSIX connection files are created with owner-only permissions. The project does not migrate existing state when a platform default changes; use an explicit override to retain an existing installation's state.

## Checking the connection

```powershell
.\.venv\Scripts\python.exe -m firestorm_mcp.probe
```

This creates a short-lived real MCP client/server pair and queries the existing bridge. It does not start a viewer, acquire/release a lease or send UI input. Exit codes: **0** connected, **2** MCP works but bridge disconnected, **1** probe failure. Optional `--output report.json` writes a local diagnostic report; review it before sharing because a connected session can include a control-owner label and process metadata.

The stdio MCP server can run while the viewer is offline. A normal Firestorm shortcut starts without LEAP. A viewer launched without the helper must be closed normally at a convenient time and started through the launcher. An occupied lease is a coordination signal, not a reason to restart.

## Wheel installation

Release wheels can be installed with `python -m pip install path/to/firestorm_mcp-0.3.0a2-py3-none-any.whl` in a dedicated environment. Use the installed `firestorm-mcp`, `firestorm-mcp-launch` and `firestorm-mcp-check` commands, or their Python module equivalents. The wheel contains the LEAP entry file, so it does not require the original checkout. Only Windows installs `pywin32`. Other dependencies are resolved for your platform. Setup and offline MCP operation are checked separately from the experimental Linux/macOS viewer integrations; consult [PLATFORMS.md](PLATFORMS.md).

This release is not published to PyPI or the public MCP Registry. While the GitHub repository is private, only authorized collaborators can retrieve release assets. When public distribution is approved, the owner can publish PyPI/registry metadata after a clean-machine install check.

## Upgrades and coexistence

Install a new release in its own folder/environment. Keep an active consumer's command, source and runtime unchanged until its owner schedules an update. Do not run two development helpers against one viewer or reset an occupied runtime. The new package does not automatically import state or change registration from a previous checkout-based installation.

A leftover `launch.lock` causes the launcher to stop. Inspect the process/session with its owner before removing a stale lock; the launcher will never remove another launcher's lock to force entry. `--dry-run` validates the launch plan without writing settings or starting a process, and still refuses if a viewer is already running.

## Read-only setup diagnostics

`firestorm-mcp-doctor` checks package versions, viewer layout, the state directory's apparent writability and Linux graphical-session variables. Exit **0** means these setup prechecks passed, **2** means something needs attention and **1** means the diagnostic itself failed. It does not read the bridge token, contact the viewer, launch anything or write a report. Its JSON omits local paths and can be reviewed for an issue report. It is not a successful LEAP connection test; use `firestorm-mcp-check` for that.

On Linux/macOS, `connection_status.local_platform.native_file_dialogs` is false. Agents must arrange manual file selection, then inspect the importer result. File-dialog controls remain in the stable catalog for compatibility but report unsupported instead of attempting Windows input. This does not establish full native-dialog, Wayland, accessibility or headless support.
