# Verification and limits

## Current package checks

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
