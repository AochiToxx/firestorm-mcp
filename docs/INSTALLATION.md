# Installation and configuration

## Windows source package

Install Python 3.11+ from python.org and Firestorm from its official distribution. Extract a release source ZIP to a permanent local folder and run `Install.cmd`. Use `Install.ps1 -Python 'C:\path\to\python.exe'` if Python is not on PATH. The installer creates `.venv`; do not copy another machine's environment. `-Development` selects editable installation and test dependencies.

Development `0.3.0a1` also updates pip inside that dedicated environment before dependency installation. This requires access to the configured package index and does not update global Python. `requirements-lock.txt` records the inspected Windows/Python 3.12 development/build dependencies; it is not a cross-platform, hash-locked runtime bundle.

The bundled scripts have no code-signing certificate. If Windows marks a downloaded archive as blocked, review its source and use the archive's Properties → Unblock before extracting it again. Follow local PowerShell policy; do not globally disable execution-policy protections. You can also run the documented Python modules directly from the installed environment.

Run `Start-FirestormMCP.cmd` when you are ready to launch the viewer. The launcher checks for any running Firestorm process and refuses a second launch. It never kills, logs out or replaces a viewer. `Start-FirestormMCP.ps1 -LoginScreen` disables saved auto-login for that launch. Without that flag the viewer retains its normal login preference. No credentials pass through this MCP.

## MCP hosts

The examples in this checkout target development `0.3.0a1`. Omit `--tool-profile compact` when configuring the older `0.2.0a1` release, which does not implement that flag. Current protocol and host verification are recorded in [COMPATIBILITY.md](COMPATIBILITY.md); a configuration example is not a claim that the host's UI has been tested.

Use the absolute environment Python path as the command and `-m firestorm_mcp.server` as arguments. A JSON example is in the README. For Codex's TOML configuration, add the following deliberately at the scope you want; no installer edits it automatically:

```toml
[mcp_servers.firestorm]
command = 'C:\path\to\firestorm-mcp\.venv\Scripts\python.exe'
args = ['-m', 'firestorm_mcp.server', '--tool-profile', 'compact']
tool_timeout_sec = 180
```

Alternatively use the Codex CLI: `codex mcp add firestorm -- C:\path\to\firestorm-mcp\.venv\Scripts\python.exe -m firestorm_mcp.server`. Check an existing entry first rather than replacing another integration. Other MCP hosts use the same stdio command with their own configuration wrapper.

Codex's per-tool timeout defaults to 60 seconds; a multi-read importer/orbit workflow can take longer. The example allows 180 seconds at the host. An individual viewer RPC still has its own bounded timeout; increasing the host timeout does not cancel or retry sent actions. See [official Codex MCP configuration](https://developers.openai.com/codex/mcp).

### Claude Desktop and Cursor on Windows

Use the following server entry in Claude Desktop's MCP configuration or Cursor's `.cursor/mcp.json`. Keep paths local to the Windows machine running Firestorm. The root object is `mcpServers`:

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

The newer Agent Host has its own configuration scope; consult the [current VS Code reference](https://code.visualstudio.com/docs/agents/reference/mcp-configuration) when using the separate Agents Window or portable Copilot configuration. Select only relevant tools when combining multiple servers: [VS Code documents a 128-tool request limit](https://code.visualstudio.com/docs/agents/run/tools). Compact mode reduces this project's listed tools to 42 but does not reserve capacity for other servers or restrict `viewer_call` authority.

### Local desktop requirement

Run the server as a Windows desktop process on the same machine and user session as the viewer. An MCP host running only in WSL, a development container, a remote SSH machine or the cloud cannot directly use the viewer's native Windows dialogs through this package. The private LEAP helper's `/rpc` URL is an internal authenticated bridge, **not** an MCP HTTP endpoint. Do not put it into a host's `url` field or expose it through a tunnel. Remote MCP transport and shared hosting are not implemented.

## Paths and alternate viewer installations

| Setting | Default | Override |
| --- | --- | --- |
| Runtime and captures | `%LOCALAPPDATA%\FirestormMCP` | `FIRESTORM_MCP_HOME` or `--data-dir` on server, launcher and probe |
| Viewer directory for UI/native helpers | `C:\Program Files\Firestorm-Releasex64` | `FIRESTORM_VIEWER_DIR` or server/probe `--viewer-dir` |
| Viewer executable for launch | `Firestorm-Releasex64.exe` in that directory | launcher `--viewer` or PowerShell `-Viewer` |

Use matching directories for the server and launcher. For a non-default viewer executable, supply both the launch executable and the server's containing viewer directory. `--root` remains an alias for the server/probe's `--data-dir`; it now means state location, not source code. Source, environment and state are separate.

The data directory contains `runtime/connection.json` (a private session token), session settings and `captures/`. Keep it machine-local and out of cloud-sync/source repositories. A non-Windows state default is available for development tests, but that does not certify macOS/Linux viewer support.

## Checking the connection

```powershell
.\.venv\Scripts\python.exe -m firestorm_mcp.probe
```

This creates a short-lived real MCP client/server pair and queries the existing bridge. It does not start a viewer, acquire/release a lease or send UI input. Exit codes: **0** connected, **2** MCP works but bridge disconnected, **1** probe failure. Optional `--output report.json` writes a local diagnostic report; review it before sharing because a connected session can include a control-owner label and process metadata.

The stdio MCP server can run while the viewer is offline. A normal Firestorm shortcut starts without LEAP. A viewer launched without the helper must be closed normally at a convenient time and started through the launcher. An occupied lease is a coordination signal, not a reason to restart.

## Wheel installation

Release wheels can be installed with `python -m pip install path/to/firestorm_mcp-0.2.0a1-py3-none-any.whl` in a dedicated environment. Use the installed `firestorm-mcp`, `firestorm-mcp-launch` and `firestorm-mcp-check` commands, or their Python module equivalents. The wheel contains the LEAP entry file, so it does not require the original checkout. Native dependencies and viewer integration still target Windows even though the pure-Python bridge wheel uses the platform-independent filename tag.

This release is not published to PyPI or the public MCP Registry. While the GitHub repository is private, only authorized collaborators can retrieve release assets. When public distribution is approved, the owner can publish PyPI/registry metadata after a clean-machine install check.

## Upgrades and coexistence

Install a new release in its own folder/environment. Keep an active consumer's command, source and runtime unchanged until its owner schedules an update. Do not run two development helpers against one viewer or reset an occupied runtime. The new package does not automatically import state or change registration from a previous checkout-based installation.

A leftover `launch.lock` causes the launcher to stop. Inspect the process/session with its owner before removing a stale lock; the launcher will never remove another launcher's lock to force entry. `--dry-run` validates the launch plan without writing settings or starting a process, and still refuses if a viewer is already running.
