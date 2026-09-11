# Verification and limits

## Current package checks

Version `0.3.0a1`, checked in isolation on 11 September 2026 with Windows/Python 3.12 and MCP SDK 2.2.0: **64 tests passed**. The Windows CI matrix also passed on Python **3.11, 3.12, 3.13 and 3.14**. Wire-level tests exercise five protocol revisions, including direct `server/discover` on `2026-07-28`, legacy handshakes, clean UTF-8 stdio, structured and PNG results, strict input rejection, catalog-change notifications in both eras, compact discovery and cancellation of a queued viewer call. Consumer regressions cover complete UI pagination, per-item inspection errors, basename/depth matching, required/hidden keyboard targets, before/after selection readback, ambiguous registry-button rejection, flat-frame detection, preview-camera bounds/targeting/cleanup and redirect refusal. These tests use temporary files and a synthetic loopback bridge; none contacts an actual viewer.

The pinned official MCP Inspector **2.6.0** independently listed 43 tools with **zero strict schema findings** and completed an offline connection-status call. The dependency advisory scan found legacy pip advisories in the freshly bootstrapped environment; updating that environment to pip 26.2.1 cleared the reported findings. The scan covered the development environment's installed third-party packages; the editable project itself was skipped by the advisory service and is covered by code/tests instead. This is a point-in-time advisory check, not proof of absence of vulnerabilities. The source installer now updates only its dedicated pip to `>=26.2,<27` before installing dependencies.

A separate **SDK v1.30.0 client** also connected to the new server over stdio, negotiated `2025-11-25`, listed 43 tools and read disconnected status. The wheel and source distribution passed `twine check`; the wheel installed in a fresh environment and passed its current-protocol offline probe with the packaged LEAP entry present. The source ZIP's Windows PowerShell installer also completed in a separate fresh environment and passed its offline MCP probe. The protocol/package checks did not contact a live viewer; the separately authorized cutover below did.

The older release record below belongs to `0.2.0a1`. Source remains separate from installed consumer environments. See the [compatibility audit](COMPATIBILITY.md).

## Coordinated candidate launcher check

The first `0.3.0a1` candidate was installed from its built wheel into a new machine-local environment. After coordinating with the consumer and acquiring the free bridge lease, the viewer was normally closed and restarted with the package's launcher. The wheel-resident LEAP helper connected; a real SDK-v2 stdio session observed `STATE_STARTED`, discovered 18 APIs / 94 operations, and retained its then-current 42 tools in compact mode. The temporary startup event subscription and control lease were released, and the client exited. The earlier installation was preserved for rollback. The later camera/search candidate exposed 43 tools and was retested by the consumer against the same running helper before the final installation update.

## Coordinated live consumer evidence

A separate consumer agent exercised an actual five-file Blender-export workflow in **Firestorm 7.2.4.80712 on Windows**, using a persistent real MCP SDK client and bounded control leases. It returned issues during testing, then tested the corrected wheel-installed server. Product-specific filenames, hashes, account details, captures and cost decisions remain in private consumer records.

| Workflow | Observed result / boundary |
| --- | --- |
| Scoped discovery and pages | Basename/prefix/glob/depth filters reached tabs and source controls with explicit page completion. A `%`-named child initially failed the whole inspected page; after the fix, all 11 paths remained and only that child's information was marked unavailable. |
| Tabs and file loading | Registered callbacks changed the visible LOD/Physics panel. Fresh native pickers loaded all four explicit LOD files and the physics file; displayed paths and settled counts matched the consumer's expectations. This is UI readback, not a cryptographic binding to uploaded bytes. |
| Source selection | Targeted Home selected `Load from file`; targeted Return committed it and made Browse visible. A selected label alone was insufficient. Both stages are documented in the agent guide. |
| Preview selection and camera | Targeted High/Lowest/High selection was read back, with visible geometry differences at Lowest and restored High in final captures without the physics overlay. Preview zoom and orbit visibly changed the rendered preview; zoom enlarged an initially tiny model for close-up inspection. Pan has synthetic coverage but was not separately live-tested. No exact camera pose or restoration was measured. |
| Physics and Analyze | Explicit physics input was read back and Analyze produced the expected hull/vertex result. This does not certify uploaded or simulator collision behavior. |
| Preview checkbox | Mouse input returned handled but left `show_physics` unchanged. A single path-targeted Space on its child button changed the parent boolean and visibly removed the overlay; the ineffective mouse path remains a documented limitation. |
| Quote lifecycle | Calculate reached settled displayed weights/fee. A temporary scale change altered dimensions and invalidated the quote; restoring the original scale and recalculating worked. Preview LOD changes also invalidated the quote. Values remain `displayed_only`, never automatically certified fresh or an authorization to upload. |
| Captures | Current nonblank preview images supported visual inspection, with metadata and hashes retained privately. Caller labels still needed correction when an import changed the preview LOD. A naturally blank/stale negative case was not exercised; synthetic detector tests remain separate evidence. |
| Cleanup | The consumer cancelled its preview, verified the floater hidden and no native picker remaining, released its own lease and exited its client. All five source hashes still matched. Original scale was restored; the final preview was cancelled with its later quote invalidated. |

No upload, simulator rez, paid action, chat or inventory change was submitted by this acceptance workflow. A working importer workflow does not pass the consumer product's cost or release gates.

## Released 0.2.0a1 package checks

Local verification on 11 September 2026 using Windows and Python 3.12: `python -m pytest -q` passed **35 tests**. The built wheel installed into a fresh temporary environment, initialized the real MCP SDK, listed 42 workflow tools and reported the deliberately isolated viewer state as disconnected (exit 2). Its packaged LEAP entry was present. Source/wheel metadata checks passed. The allowlisted source ZIP and tracked-file review excluded private runtime and consumer evidence. CI runs isolated tests; no GitHub job should connect to a real viewer or user account.

Tests cover byte-counted binary/notation LLSD, fragmented input, exact duplicate-block recovery, malformed frames, reply correlation and late replies, lease ownership, loopback authentication/Origin rejection, native-dialog rejection, metadata and image comparison, unknown/hidden UI fields, displayed quote freshness boundaries, real SDK stdio initialization and package launch safeguards.

## Inherited live evidence

The predecessor integration was tested on Windows with Firestorm 7.2.4.80712. Those results are inherited, not repeated live for this package:

- Original synthetic cube imported into Local Mesh and the model-upload preview: 12 triangles, 24 vertices, dimensions 1.000 × 1.000 × 1.000, uncalculated fee.
- Exact ASCII text replacement readback and restoration; a named viewer setting changed, read back and restored.
- Registered-panel discovery, scoped UI queries and recognized native file selection.
- Avatar position, nearby-object and scoped inventory queries returned viewer data.
- Two requested world-camera poses produced visually different 1280 × 720 images and capture manifests; scripted camera was released, not restored to the exact earlier manual pose.
- Forty large scoped UI queries completed with nine exact duplicated 4 KiB pipe blocks recovered, zero failed queries and zero decode errors.

No paid upload or simulator rez was submitted for those synthetic bridge tests. Private raw scene captures and session reports are deliberately absent from this repository. These summaries do not certify any consumer product or every discovered viewer operation.

## Remaining validation boundaries

The packaged launcher and the bounded consumer importer workflow have been live-checked as described above. This does not cover every field, warning condition, operation or failure mode. Combo/checkbox behavior remains version-dependent; pan, naturally blank/stale captures, deliberately unsafe-focus negative cases and other MCP host applications and viewer/OS combinations still need their own live acceptance checks. The two-candidate consumer session took approximately 46 minutes, including coordination; that exceeded its planned 45-minute window by about a minute and is not a performance benchmark.

Do not claim universal Firestorm compatibility, complete object/material/permission readback, guaranteed cancellation, exact camera restoration, fresh quote binding or simulator asset acceptance. See the README limitations and tool descriptions.
