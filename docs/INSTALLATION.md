# Installation

Download the [0.3.0a3 setup ZIP](https://github.com/AochiToxx/firestorm-mcp/releases/tag/v0.3.0a3) and extract it into a permanent, user-writable folder. Install Python **3.11–3.14** separately, plus Firestorm for live viewer control. Installation needs access to your Python package index.

## Quick setup

Run these from the extracted folder. On Windows, double-click `.cmd` files or prefix local scripts with `.\` in PowerShell:

| Action | Windows | Linux / macOS |
| --- | --- | --- |
| Install | `Install.cmd` | `sh Install.sh` |
| Print MCP configuration | `.venv/Scripts/python.exe -m firestorm_mcp.configure` | `.venv/bin/python -m firestorm_mcp.configure` |
| Check setup offline | `.venv/Scripts/python.exe -m firestorm_mcp.doctor` | `.venv/bin/python -m firestorm_mcp.doctor` |
| Launch viewer | `Start-FirestormMCP.cmd` | `sh Start-FirestormMCP.sh` |
| Check connection | `Check-FirestormMCP.cmd` | `sh Check-FirestormMCP.sh` |

The installer creates `.venv`, updates pip there and prints configuration. It does not edit agent settings or start Firestorm. Windows keeps the installer output open until you press a key.

For unattended setup, use `python install.py` or `python3 install.py`. Add `--development` for editable source and test dependencies. Select another interpreter with `.\Install.ps1 -Python 'C:/path/to/python.exe'` or `PYTHON=/path/to/python3 sh Install.sh`.

## Agent configuration

Merge the generated entry into your host's settings, keeping other servers and **all generated arguments**.

| Host | Generator option | Configuration format |
| --- | --- | --- |
| Claude Desktop / Cursor | `--format json` (default) | `mcpServers.firestorm` |
| Codex | `--format codex` | `[mcp_servers.firestorm]` in the intended TOML scope |
| VS Code extension host / Copilot | `--format vscode` | `servers.firestorm` in `.vscode/mcp.json` |
| CLI-configured hosts | Default JSON supplies the command/args | Register the complete command as a local stdio server |

Example for Codex on Linux/macOS:

```sh
.venv/bin/python -m firestorm_mcp.configure --format codex
```

On Windows, use `.venv/Scripts/python.exe` instead. Add the same `--viewer` and `--data-dir` selections used for launch. The generator preserves absolute paths and the virtual environment, including when a desktop host has a different PATH.

Codex output allows 180 seconds per tool. Viewer RPC timeouts remain separate. Generated formats are checked; host application UIs are not all tested. See the official guides for [Codex](https://developers.openai.com/codex/mcp), [Cursor](https://cursor.com/docs/mcp), [Claude Code](https://code.claude.com/docs/en/mcp) and [VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration). VS Code's separate Agent Host may use another scope.

## Choose a viewer

Conventional installation locations are detected automatically. If none or several are found, pass `--viewer` to both configuration and launch:

```sh
# Linux: select the supplied wrapper, not the internal binary.
.venv/bin/python -m firestorm_mcp.configure --viewer /opt/firestorm/firestorm
sh Start-FirestormMCP.sh --viewer /opt/firestorm/firestorm

# macOS: use the actual installed .app name.
.venv/bin/python -m firestorm_mcp.configure --viewer /Applications/Firestorm-Releasex64.app
sh Start-FirestormMCP.sh --viewer /Applications/Firestorm-Releasex64.app
```

```powershell
# Windows: select the installed executable.
.venv/Scripts/python.exe -m firestorm_mcp.configure --viewer 'D:/Apps/Firestorm/Firestorm-Releasex64.exe'
.\Start-FirestormMCP.cmd --viewer 'D:/Apps/Firestorm/Firestorm-Releasex64.exe'
```

Merge the regenerated configuration after changing viewer paths. `FIRESTORM_VIEWER` is an environment alternative, but GUI hosts may not inherit shell exports.

Use `--dry-run` to validate without starting/writing, or `--login-screen` to disable saved auto-login for one launch. The PowerShell wrapper uses `-Viewer`, `-DataDir`, `-DryRun` and `-LoginScreen` instead.

The launcher refuses a running Firestorm process or an existing launch lock. Arrange a normal close when convenient; LEAP cannot attach after viewer startup. Leave another agent's lease or lock alone.

## State and resources

| OS | Default state/captures | Viewer resources |
| --- | --- | --- |
| Windows | `%LOCALAPPDATA%\FirestormMCP` | Executable's folder |
| macOS | `~/Library/Application Support/FirestormMCP` | `.app/Contents/Resources` |
| Linux | `$XDG_STATE_HOME/firestorm-mcp`, or `~/.local/state/firestorm-mcp` | Distribution wrapper's folder |

Override state with `FIRESTORM_MCP_HOME` or matching `--data-dir` arguments on configure, launch and check. Quoted `~` paths are expanded. `--root` remains a server/probe alias for `--data-dir`.

Generated config sets `--viewer-dir` when a viewer is found. `FIRESTORM_VIEWER_DIR` also overrides resources; keep it matched to the selected viewer. Without an installed viewer, generated config leaves discovery enabled for later.

State includes a private session token and captures. Keep it machine-local and out of source control/cloud sync. POSIX token files are owner-only. Existing state is not migrated automatically.

## Troubleshooting

| Symptom | Next step |
| --- | --- |
| Python or `venv` missing | Select Python 3.11+. Debian/Ubuntu/Pi OS may need `python3-venv`. |
| Dependency build fails | Check OS/CPU wheels and build prerequisites in [PLATFORMS.md](PLATFORMS.md). Use the installer, not the historical Windows lock snapshot. |
| Viewer not found or ambiguous | Supply the exact `--viewer` path and regenerate config. |
| MCP works, viewer disconnected | Start through the launcher in the same desktop user session, then run the connection check. |
| `.venv` is incomplete, moved or from another OS | Extract a fresh folder and reinstall. Do not copy environments between systems. |

The **doctor** is offline: exit 0 means setup prechecks passed, 2 means attention is needed, 1 means it failed. Its report omits private paths and tokens.

The **connection check** queries the bridge without acquiring a lease or sending UI input: exit 0 means connected, 2 means MCP works but the viewer is disconnected, 1 means failure. An optional `--output report.json` may include control-owner/process details; review it before sharing.

The scripts are unsigned. Follow local execution policy; the Python modules can be run directly. Use a user-writable installation, without `sudo pip` or global Python changes.

## Wheels and upgrades

Install the release wheel with `python -m pip install path/to/firestorm_mcp-0.3.0a3-py3-none-any.whl` inside a dedicated environment. It includes the LEAP helper and the `firestorm-mcp`, `firestorm-mcp-launch`, `firestorm-mcp-check`, `firestorm-mcp-config` and `firestorm-mcp-doctor` commands.

Install upgrades in a new folder/environment. Coordinate an active consumer's switch; builds do not update its configuration automatically. Keep the earlier environment for rollback.

Live control needs a local desktop. Remote MCP transport and non-Windows native pickers are not implemented. The internal `/rpc` URL is not an MCP endpoint; do not expose it. [Platform support](PLATFORMS.md).
