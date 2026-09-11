# Verification and limits

## Current package checks

Development `0.3.0a1`, checked in isolation on 11 September 2026 with Windows/Python 3.12 and MCP SDK 2.2.0: **45 tests passed**. New wire-level tests exercise five protocol revisions, including direct `server/discover` on `2026-07-28`, legacy handshakes, clean UTF-8 stdio, structured and PNG results, strict input rejection, catalog-change notifications in both eras, compact discovery and cancellation of a queued viewer call. These tests use temporary files and a synthetic loopback bridge; none contacts an actual viewer.

The pinned official MCP Inspector **2.6.0** independently listed 42 tools with **zero strict schema findings** and completed an offline connection-status call. The dependency advisory scan found legacy pip advisories in the freshly bootstrapped environment; updating that environment to pip 26.2.1 cleared the reported findings. The scan covered the development environment's installed third-party packages; the editable project itself was skipped by the advisory service and is covered by code/tests instead. This is a point-in-time advisory check, not proof of absence of vulnerabilities. The source installer now updates only its dedicated pip to `>=26.2,<27` before installing dependencies.

A separate **SDK v1.30.0 client** also connected to the new server over stdio, negotiated `2025-11-25`, listed 42 tools and read disconnected status. The development wheel and source distribution passed `twine check`; the wheel installed in a fresh temporary environment and passed its current-protocol offline probe with the packaged LEAP entry present. No running viewer, shared configuration or consumer installation was modified.

The release record below belongs to `0.2.0a1`; it must not be treated as live acceptance of the development migration. The new source is kept separate from active consumer installations. See the [compatibility audit](COMPATIBILITY.md).

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

## Still needs live validation in this release

The packaged launcher now uses a wheel-resident LEAP entry and machine-local state. Its refusal/dry-run/path logic is automated-tested, but its new launch path must be verified on an explicitly available viewer session. Expanded importer file/source/weight/fee visibility fields have simulated regression coverage and installed-XUI evidence; all fields have not been live-certified. Exact combo-box selection remains a version-dependent UI workflow.

Do not claim universal Firestorm compatibility, complete object/material/permission readback, guaranteed cancellation, exact camera restoration, fresh quote binding or simulator asset acceptance. See the README limitations and tool descriptions.
