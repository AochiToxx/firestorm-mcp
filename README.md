# Firestorm MCP

**Give AI agents structured tools for the Firestorm viewer: inspect 3D exports, drive mesh previews, control the camera and collect verification evidence in Second Life.**

[Downloads](#downloads) · [Install](#install-on-windows) · [Capabilities](#what-can-it-do-today) · [Agent quick start](#for-ai-agents) · [Tool reference](docs/TOOLS.md) · [Contribute](CONTRIBUTING.md) · [Known limits](#known-limits)

**Version:** `0.3.0a1` · Windows alpha · Python 3.11–3.14 tested · MIT licence

This release adds MCP SDK v2 and protocol compatibility through `2026-07-28`, a compact tool profile, structured results, precise paged UI searches, path-targeted keys, registered button callbacks, uploader camera input and blank-capture detection. See the [compatibility audit and remaining work](docs/COMPATIBILITY.md).

Firestorm MCP is an independent, community-oriented **Model Context Protocol (MCP)** server. It connects to an installed Firestorm viewer through the viewer's **LEAP** interface. Your agent works through the same viewer you can see and control; no separate bot avatar or custom viewer build is required.

It is useful for Blender-to-Second-Life iteration, importer diagnostics, repeatable scene captures, viewer UI automation and building better agent workflows. Each user runs their own local installation. This project does not provide a shared remote viewer service.

```text
Your AI agent / MCP host
        │ MCP over stdio
        ▼
Firestorm MCP server
        │ authenticated loopback connection
        ▼
Viewer-owned LEAP helper ────── Firestorm viewer ────── Second Life
```

The catalog defines **43 workflow tools**. A tested, signed-in Firestorm **7.2.4.80712** session exposed **94 additional operations across 18 APIs**; with the current workflow catalog, that gives **137 tools** in the expanded profile. Before login, fewer operations are available. These are discovery counts, not a claim that every consequential operation has been live-tested. Always refresh capabilities on the viewer you actually use.

Startup exposes the 43 workflow tools immediately, even with a stalled viewer. Call `capabilities_refresh` to discover viewer operations. Use `--tool-profile compact` when combining this server with other MCPs or using hosts with tool-count limits: the list stays at 43 and `viewer_call` retains access to all discovered operations. The default `all` profile adds individual viewer tools after refresh. Compact mode changes discovery presentation, not permissions.

## Downloads

**[Download Firestorm MCP for Windows — setup/source ZIP](https://github.com/AochiToxx/firestorm-mcp/releases/download/v0.3.0a1/firestorm-mcp-0.3.0a1-source.zip)**

| Download | Choose this when |
| --- | --- |
| [Windows setup/source ZIP](https://github.com/AochiToxx/firestorm-mcp/releases/download/v0.3.0a1/firestorm-mcp-0.3.0a1-source.zip) | Recommended: extract, run `Install.cmd`, then follow the quick start. Includes source, setup scripts, docs and tests. Python and Firestorm are installed separately. |
| [Python wheel](https://github.com/AochiToxx/firestorm-mcp/releases/download/v0.3.0a1/firestorm_mcp-0.3.0a1-py3-none-any.whl) | You already manage Python environments and want the installed command-line tools. |
| [SHA-256 checksums](https://github.com/AochiToxx/firestorm-mcp/releases/download/v0.3.0a1/SHA256SUMS.txt) | Verify a downloaded asset against the published release. |
| [Release notes and all assets](https://github.com/AochiToxx/firestorm-mcp/releases/tag/v0.3.0a1) | Review this alpha's changes, checks and limitations. |

Downloads are hosted on this project's GitHub Releases page. They require repository access while the project remains private. This alpha is not yet listed on PyPI or the public MCP Registry.

## Install on Windows

1. Install **Python 3.11 or newer** from [python.org](https://www.python.org/downloads/windows/) and the normal [Firestorm viewer](https://www.firestormviewer.org/). Python must be available as `python` in your terminal.
2. Download the source ZIP from [Releases](https://github.com/AochiToxx/firestorm-mcp/releases), or choose **Code → Download ZIP**. Extract it to a permanent local folder. While this repository is private, GitHub access is required to download it.
3. Run **`Install.cmd`**. This creates a dedicated Python environment and installs the MCP. It does not change your agent configuration or start Firestorm.
4. When you are ready to begin a viewer session, run **`Start-FirestormMCP.cmd`**. Sign in normally in Firestorm. The launcher refuses to replace a running Firestorm process.
5. Add the MCP command shown below to your agent's MCP configuration. Run **`Check-FirestormMCP.cmd`** to verify the connection.

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

Replace the example path with the folder you extracted. The MCP host must support local **stdio** servers. The JSON wrapper varies by host; the command and arguments are the same. For Codex, see [installation and configuration](docs/INSTALLATION.md). The server itself also exposes `firestorm-mcp`, `firestorm-mcp-launch` and `firestorm-mcp-check` console commands in its installed environment.

**Already running Firestorm?** Coordinate a normal close and launcher start when your session is safe to end. LEAP connects at viewer startup; the helper cannot attach retroactively. Starting or reconnecting the MCP server alone does not start the viewer. Do not interrupt another agent's viewer session to refresh tool discovery.

The new package stores runtime state under `%LOCALAPPDATA%\FirestormMCP` by default, separate from the checkout and installed code. Use `FIRESTORM_MCP_HOME` or matching `--data-dir` arguments on the launcher/server/check command to choose another machine-local directory. See [configuration, upgrades and troubleshooting](docs/INSTALLATION.md).

## What can it do today?

| Area | Workflow tools | What you can obtain or do |
| --- | --- | --- |
| Connection and discovery | `connection_status`, `capabilities_refresh`, `viewer_api_inspect`, `viewer_call` | Check the bridge and discover the running viewer's actual APIs and argument descriptions. Invoke a discovered operation through a generic entry point. |
| Shared control | `control_acquire`, `control_release` | Hold a bounded, renewable control lease across a multi-step workflow. A foreign client cannot take over an active lease. Human input remains possible. |
| Events | `events_subscribe`, `events_read`, `events_unsubscribe` | Subscribe to named viewer event streams, read cursor-based results and detect dropped buffered events. |
| Export files | `asset_inspect` | Read COLLADA/glTF/GLB/image metadata, hashes, DAE units/axis/declared triangles, material counts or definitions and image references. No Blender process is required. |
| Local mesh preview | `local_mesh_open`, `local_mesh_status`, `local_mesh_auto_reload` | Open Firestorm Local Mesh, inspect its selection/log and configure automatic reload with previous-setting readback. A local replacement is visible only in that viewer. |
| Mesh importer | `mesh_upload_open`, `mesh_upload_status`, `mesh_preview_camera` | Open the model-upload preview; read LOD source/file selections, counts, dimensions, physics, warnings, displayed weights/costs and visibility; adjust the separate preview camera with a bounded path-targeted drag. Reading status neither calculates nor submits an upload. |
| Native file selection | `native_file_dialogs`, `native_file_choose` | Discover recognized Windows Open dialogs owned by Firestorm, select an existing file and verify filename readback before invoking Open. Requires normal desktop access. |
| Panels and UI | `floater_list`, `floater_open`, `ui_find`, `ui_inspect`, `ui_get_value`, `ui_click`, `ui_set_text`, `ui_press_key`, `ui_select` | Search paths or names with exact/prefix/glob/depth filters and explicit pages; inspect visibility/enabled state; invoke unique registered button callbacks; send path-targeted keys with before/after readback. Selection by value depends on the viewer version. |
| Menus | `ui_list_menus`, `ui_invoke_menu` | Inspect installed menu definitions and invoke an exact validated entry. Arbitrary callbacks are rejected. |
| Avatar movement | `avatar_position`, `avatar_walk_to`, `avatar_movement_status`, `avatar_stop` | Read position, start/poll/stop autopilot. Walking takes global coordinates; successful dispatch does not prove arrival. |
| Nearby objects and inventory | `world_objects`, `inventory_search` | Query nearby object IDs/positions and search a specific inventory folder. This is not full object, face or permission inspection. |
| Camera and evidence | `camera_set`, `camera_release`, `snapshot`, `capture_orbit`, `capture_manifest_read`, `image_compare` | Request region-coordinate camera poses, capture PNGs with hashes and blank-frame flags, save orbit manifests and calculate pixel differences between same-sized images. Nonblank images still require visual review. |
| Viewer settings | `setting_get`, `setting_set` | Read/change a named setting with before/after readback. Restore temporary settings yourself; some persist across sessions. |

The **dynamic viewer tools** add the operations exposed by these APIs: `GroupChat`, `LLAgent`, `LLAppViewer`, `LLAppearance`, `LLCommandDispatcher`, `LLFloaterAbout`, `LLFloaterReg`, `LLGesture`, `LLInventory`, `LLNotifications`, `LLPipeline`, `LLStartUp`, `LLTeleportHandler`, `LLURLDispatcher`, `LLViewerControl`, `LLViewerWindow`, `LLWindow` and `UI`.

Those operations cover capabilities such as teleporting, touch/sit/stand requests, animations, outfits, gestures, group chat, notifications, render toggles and viewer shutdown. **Availability is not authorization:** an agent must have the user's authority for each consequential workflow. Discovery does not verify all of these functions or every possible argument.

Dynamic names follow `viewer_<API>_<operation>` and take viewer fields inside `arguments`. For example, inspect an operation with `viewer_api_inspect` before using `viewer_call`. Exact schemas are in [tool-catalog.json](docs/tool-catalog.json); the historical viewer descriptors are in [viewer-api-reference.json](docs/viewer-api-reference.json). The running viewer is the authority when these differ.

## For AI agents

**Start here; do not infer success from a tool's name or a dispatched input.**

1. Call `connection_status {}`. If disconnected, report it. Starting the server and starting the viewer are different actions.
2. Call `capabilities_refresh {}` and inspect unfamiliar operations with `viewer_api_inspect`.
3. Acquire `control_acquire {"label":"describe the workflow","seconds":300}`. Keep all related calls in the same MCP session, renew before expiry and release in `finally`. A busy lease means coordinate with its owner.
4. Discover relevant UI paths with `floater_open` and scoped `ui_find`. Inspect visibility/enabled state before input. Whole-viewer UI enumeration can include a large inventory tree.
5. Read back results and capture evidence. Record whether the result is source metadata, UI readback, a viewer-local preview or verified simulator state.
6. Restore temporary settings where supported and call `control_release {}`. Do not claim that `camera_release` restores the previous manual camera pose.

If native tool discovery is missing from your current agent session, the **real MCP SDK fallback** in [the agent guide](docs/AGENT_GUIDE.md) connects directly without restarting your agent application. `python -m firestorm_mcp.probe` tests this entry point without taking a lease or sending UI input.

### Example: inspect a model without submitting an upload

```text
asset_inspect {"filename":"C:/exports/example-high.dae"}
control_acquire {"label":"Mesh importer inspection","seconds":300}
mesh_upload_open {}
native_file_dialogs {}
native_file_choose {"dialog_id":<fresh discovered ID>,"filename":"C:/exports/example-high.dae"}
mesh_upload_status {}
... inspect settled preview state and capture evidence ...
control_release {}
```

Choose the originating file dialog deliberately. Some texture, sound or animation upload workflows can advance toward upload when a file is selected. The example above refers to **model importer preview**. Paid uploads, purchases, transfers, deletion, messages and unrelated world edits require separate authority. Local Mesh's **Rez Selected** control creates simulator objects.

## Evidence and verification

The inherited viewer integration was live-tested on Windows with Firestorm **7.2.4.80712**. An original synthetic cube was loaded into Local Mesh and model-upload preview: **12 triangles, 24 vertices and 1 × 1 × 1 dimensions**. Text replacement/readback/restoration, a setting change/restoration, camera captures, scoped UI queries and native file selection were exercised. A 40-query large-reply run recovered nine duplicated Windows pipe blocks with zero failed queries.

The wheel-installed launcher/helper was exercised through a coordinated normal viewer restart. A separate consumer agent then tested an actual five-file Blender-export importer workflow and retested fixes: scoped discovery, explicit LOD/physics loading, source commits, preview selection, zoom/orbit, checkbox readback, Analyze, capture inspection and quote invalidation. Automated validation includes **64 tests**, Windows CI on **Python 3.11–3.14**, five wire-protocol revisions, legacy/current clients and **zero strict schema findings** from the official MCP Inspector. Fresh wheel and source-installer checks also passed. See [VALIDATION.md](docs/VALIDATION.md) for exact observations and untested cases.

Raw user captures, account/object identifiers, credentials, machine paths and product assets are not distributed. Contributors should supply synthetic fixtures or minimal scrubbed reproductions.

## Known limits

- **Windows alpha.** Native file-dialog automation recognizes English common dialogs. Other OS/viewer combinations are not certified; transport-only tests on another OS do not certify its viewer integration.
- **UI selection is version-dependent.** The tested viewer lacks `UI.setSelectedByValue`, so `ui_select` reports unavailable. `ui_press_key` requires a visible enabled target `path` and returns readback; this is a breaking change from the original helper. A handled mouse click may leave a combo or checkbox unchanged. The [agent guide](docs/AGENT_GUIDE.md) records tested commit and checkbox-key procedures. Human input and viewer shortcuts can still interfere; verify state and do not blindly retry keys.
- **Capture flags are heuristic.** Uniform/black/transparent frames are flagged, but a nonblank image can still be stale, obstructed or show the wrong subject. Inspect the image before using it as verification evidence.
- **ASCII text fallback.** On the tested viewer, printable ASCII entry is supported up to 2,048 characters. Unicode/multiline paste requires another supported viewer API or user input.
- **Camera requests are not measured poses.** No exact camera getter/manual-pose restoration or dedicated FOV workflow is provided. `mesh_preview_camera` uses bounded UI drags in the uploader's separate preview; inspect fresh captures to verify the result.
- **No finished five-file import helper.** Explicit LOD/physics selection currently uses inspected UI controls and native file dialogs. Displayed filenames are not proof that particular file bytes were loaded.
- **Quotes are displayed readback.** `mesh_upload_status` labels numeric fees `displayed_only`, with `freshness_verified:false` and `calculation_requested:false`. Readback is sequential, not atomic. Hidden control text can be stale; inspect its visibility.
- **No semantic object/face/material or script lifecycle suite yet.** Nearby-object queries do not establish ownership, permissions, material assignment or land impact. Metadata inspection does not prove PBR fidelity.
- **Cancellation is limited.** A timeout or cancelled MCP request does not retract an action already sent to the viewer. Reinspect before retrying a write. `avatar_stop` specifically stops autopilot.
- **Cooperative leases.** They coordinate bridge clients but do not block human input. Generic controls remain powerful; this alpha does not enforce a universal no-spend policy in every low-level operation.

## People and AI agents: collaborate with us

**Human developers, Second Life creators, testers and AI coding agents are welcome.** Help improve this general-purpose Firestorm MCP for every consumer. Useful contributions include reproducible bugs, clearer setup docs, viewer-version testing, reliable UI primitives, mesh/physics/material readback, camera controls and safer operation lifecycle handling.

Use [Issues](https://github.com/AochiToxx/firestorm-mcp/issues) for actionable reports and [Discussions](https://github.com/AochiToxx/firestorm-mcp/discussions) for questions, ideas and examples. Read [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md), then propose a focused pull request. Include exact tool arguments, expected/observed results, tests and whether a claim was simulated or observed in a real viewer. Keep consumer products, private assets and business rules outside the generic API.

AI contributions should have a responsible human owner. Agents can propose and test improvements; maintainers review changes before they become a release. The repository starts private for review. These collaboration links require access until the owner chooses to make it public; invitations in this README do not grant repository access automatically.

## Development

```powershell
git clone https://github.com/AochiToxx/firestorm-mcp.git
cd firestorm-mcp
.\Install.ps1 -Development
.\.venv\Scripts\python.exe -m pytest -q
```

Automated tests use synthetic fixtures and isolated temporary roots. Do not run the test suite against someone else's live viewer. Use one checkout per contribution and keep production installations on a tested release until an update is deliberately scheduled.

## Licence and attribution

The bridge is [MIT licensed](LICENSE). See [THIRD_PARTY.md](THIRD_PARTY.md) for dependencies and upstream references. This project is **not affiliated with or endorsed by the Firestorm team or Linden Lab**. Install Firestorm separately from its official distribution; this repository does not redistribute the viewer or its proprietary components. Firestorm and Second Life names identify compatibility.
