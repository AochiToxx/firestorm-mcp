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

The common Python installer creates `.venv`, upgrades only that environment's pip and installs the package. It prints ready-to-copy JSON; it never edits agent configuration or starts Firestorm. Merge its `firestorm` entry into your host's configuration, keeping other servers. Host-specific wrappers are below. `--development` requests an editable installation with test dependencies.

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

Regenerate/merge the printed config after selecting another viewer. Add matching `--data-dir` options to configure/launch/check if you choose a different state directory (`-DataDir` in the PowerShell wrapper). `FIRESTORM_VIEWER` is an environment alternative to `--viewer`; GUI hosts do not necessarily inherit shell exports, which is why generated config uses explicit resource/state paths.

The launcher validates the layout, leaves a running viewer alone and refuses an existing launch lock. `--dry-run` validates without launching/writing; `--login-screen` requests the login screen while normal launches retain the viewer's login preference. The Windows PowerShell equivalents are `-DryRun` and `-LoginScreen`. LEAP must start with the viewer; starting the MCP alone cannot attach to an existing normal viewer session.

## MCP hosts

The examples target `0.3.0a2` (the same runtime flags are available in `0.3.0a1`). Omit `--tool-profile compact` when configuring the older `0.2.0a1` release, which does not implement that flag. Current protocol and host verification are recorded in [COMPATIBILITY.md](COMPATIBILITY.md); a configuration example is not a claim that the host's UI has been tested.

Use the absolute environment Python path as the command and `-m firestorm_mcp.server` as arguments. A JSON example is in the README. For Codex's TOML configuration, add the following deliberately at the scope you want; no installer edits it automatically:

```toml
[mcp_servers.firestorm]
command = 'C:\path\to\firestorm-mcp\.venv\Scripts\python.exe'
args = ['-m', 'firestorm_mcp.server', '--tool-profile', 'compact']
tool_timeout_sec = 180
```

Alternatively use the Codex CLI: `codex mcp add firestorm -- C:\path\to\firestorm-mcp\.venv\Scripts\python.exe -m firestorm_mcp.server --tool-profile compact`. Check an existing entry first rather than replacing another integration. Other MCP hosts use the same stdio command with their own configuration wrapper.

Codex's per-tool timeout defaults to 60 seconds; a multi-read importer/orbit workflow can take longer. The example allows 180 seconds at the host. An individual viewer RPC still has its own bounded timeout; increasing the host timeout does not cancel or retry sent actions. See [official Codex MCP configuration](https://developers.openai.com/codex/mcp).

### Claude Desktop and Cursor

Use the following server entry in Claude Desktop's MCP configuration or Cursor's `.cursor/mcp.json`. Use the command/args printed by `firestorm-mcp-config` on the machine running Firestorm; the Windows path below is only an example. The root object is `mcpServers`:

```json
{
  "mcpServers": {
    "firestorm": {
      "command": "C:/path/to/firestorm-mcp/.venv/Scripts/python.exe",
      "args": ["-m", "firestorm_mcp.server", "--tool-profile", "compact"]
    }
  }
}
```

See [Cursor's MCP guide](https://cursor.com/docs/mcp) and the [official local-server guide](https://modelcontextprotocol.io/docs/develop/connect-local-servers). Launching a server through a desktop application can use a different PATH from your terminal; the absolute Python path avoids that ambiguity.

### Claude Code

From PowerShell, use [Claude Code's stdio registration](https://code.claude.com/docs/en/mcp):

```powershell
claude mcp add --transport stdio firestorm -- 'C:/path/to/firestorm-mcp/.venv/Scripts/python.exe' -m firestorm_mcp.server --tool-profile compact
```

### VS Code / Copilot

For the VS Code extension host, `.vscode/mcp.json` uses `servers`, not `mcpServers`:

```json
{
  "servers": {
    "firestorm": {
      "type": "stdio",
      "command": "C:/path/to/firestorm-mcp/.venv/Scripts/python.exe",
      "args": ["-m", "firestorm_mcp.server", "--tool-profile", "compact"]
    }
  }
}
```

The newer Agent Host has its own configuration scope; consult the [current VS Code reference](https://code.visualstudio.com/docs/agents/reference/mcp-configuration) when using the separate Agents Window or portable Copilot configuration. Select only relevant tools when combining multiple servers: [VS Code documents a 128-tool request limit](https://code.visualstudio.com/docs/agents/run/tools). Compact mode reduces this project's listed tools to 43 but does not reserve capacity for other servers or restrict `viewer_call` authority.

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
