# Verification record

Automated checks use temporary state and simulated transports. Live viewer results are recorded separately; passing package tests does not certify a platform's desktop behavior.

## Package and protocol checks

The current suite has **85 tests**. Eight CI jobs cover Windows Python 3.11–3.14 and Python 3.12 on Linux x64/ARM64 and macOS Intel/ARM64. Python 3.12 jobs also check fresh source/wheel installs, the official MCP Inspector and dependency advisories.

| Release | Recorded checks |
| --- | --- |
| [0.3.0a3](https://github.com/AochiToxx/firestorm-mcp/releases/tag/v0.3.0a3) | Public language/description update. See its release notes for the final CI run. Runtime behavior and argument schemas are unchanged. |
| [0.3.0a2](https://github.com/AochiToxx/firestorm-mcp/actions/runs/34688862642) | All 85 tests and eight jobs passed. Fresh source/wheel installs and downloaded artifact hashes passed. |
| Skill 0.1.0 | Format/schema examples and deterministic package checks passed. Two offline instruction reviews corrected ownership, hidden-preview and restoration guidance. |
| 0.3.0a1 | 64 tests, four Windows Python jobs, fresh installs and Inspector 2.6.0 with zero strict schema findings. A separate SDK v1.30.0 client negotiated `2025-11-25`, listed 43 tools and read disconnected status. |
| 0.2.0a1 | 35 tests, fresh wheel initialization with 42 tools, packaged helper and source/wheel metadata checks. |

Coverage includes five wire-protocol revisions, UTF-8 paths, structured/PNG results, discovery notifications, input rejection, compact profiles, leases, cancellation of queued calls, UI pagination, targeted input, image flags and redirect refusal.

Portability cases cover viewer layouts, dry-runs, busy processes, foreign locks, resource paths, ambiguous discovery, host formats, quoted-home paths and offline diagnostics. Source-install tests handle macOS path aliases and use generated arguments. Launch tests record synthetic process calls; they do not start Firestorm.

An offline consumer review corrected four setup issues: dropped host arguments, inconsistent home expansion, disappearing Windows installer output and a platform-ambiguous picker example. Dependency scans cover known advisories at the time of the run.

## Live Windows workflow

The `0.3.0a1` launcher/helper and importer workflow were exercised on **Firestorm 7.2.4.80712**, using a persistent MCP client and bounded leases. A consumer agent loaded four explicit LOD files and one physics file, reported failures, then retested fixes.

| Workflow | Observed result |
| --- | --- |
| Discovery and import | Scoped/paged queries found controls. Registered callbacks switched tabs. Fresh Windows pickers loaded the five inputs; displayed paths and settled counts matched expectations. |
| Selection and physics | Home selected `Load from file`; Return committed it. Physics Analyze returned hull/vertex counts. A targeted Space changed the physics checkbox after mouse input had no effect. |
| Preview and camera | High/Lowest/High selections were read back and visually compared. Zoom and orbit changed the preview. Pan has synthetic coverage only. |
| Quotes and captures | Calculate produced displayed weights/fee. Scale and preview-LOD changes invalidated the quote. Nonblank images were inspected, with hashes kept privately. |
| Cleanup | The preview was cancelled, no picker remained, the lease was released and all five source hashes matched. Temporary scale was restored. |

These checks submitted no upload, rez, payment, chat or inventory change. They verify a local importer workflow, not simulator collision, uploaded bytes or a product's release quality.

## Earlier live checks

- An original cube loaded into Local Mesh and the model importer: **12 triangles, 24 vertices, 1 × 1 × 1 dimensions**.
- ASCII text and a viewer setting were changed, read back and restored.
- Avatar position, nearby objects and scoped inventory queries returned viewer data.
- Two world-camera requests produced different 1280 × 720 captures; scripted camera control was released.
- Forty large UI queries recovered nine duplicated 4 KiB pipe blocks, with zero failed queries or decode errors.

## Limits of this evidence

Live tests do not cover Linux/macOS/Pi, every host application or every discovered operation. Exact camera pose/restoration, fresh quote-to-file binding, full object/material/permission inspection and guaranteed cancellation remain unavailable.

The skill reuses tested procedures; host activation and a new skill-driven live benchmark remain unverified. No timing from a coordinated consumer session should be treated as a performance benchmark.

Private captures, session tokens, account/object identifiers and product records are excluded. For reproducible platform tests, use [PLATFORMS.md](PLATFORMS.md).
