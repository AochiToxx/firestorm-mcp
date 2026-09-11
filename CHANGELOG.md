# Changelog

## 0.3.0a1 — compatibility development (unreleased)

- Migrate to official MCP Python SDK v2 while retaining legacy-client protocol support.
- Initialize/discover without contacting the viewer; discover live APIs explicitly through `capabilities_refresh`.
- Add `--tool-profile compact` to keep discovery at 42 workflow tools while retaining generic API access.
- Advertise and deliver catalog changes to legacy clients and modern subscription listeners, with deterministic ordering and private zero-TTL cache hints.
- Return structured results alongside existing JSON text/images; reject invalid/extra arguments before dispatch and report unknown tools as protocol errors.
- Add wire-level checks across five protocol revisions, host-specific setup guidance and a cited compatibility audit.
- Update pip inside the dedicated installation environment before resolving project packages; add a pinned independent Inspector check to CI.
- Add basename/exact/prefix/glob UI searches, depth limits and explicit pagination/truncation.
- Add `ui_click` registered-floater callbacks with unique-path validation and optional before/after observation.
- Require a visible enabled target `path` in `ui_press_key` (breaking safety change); target both key events and return selected-value readback. Selection by value also returns readback where supported.
- Flag black, nearly uniform and transparent captures without treating nonblank images as semantic verification.
- Refuse loopback HTTP redirects so bridge credentials/actions cannot follow a redirected endpoint.
- Keep the existing release downloads and active consumer installations unchanged pending coordinated live validation.

## 0.2.0a1 — private collaboration alpha

- Package the general-purpose bridge for source and wheel installation.
- Store runtime/captures outside the checkout using machine-local state with explicit overrides.
- Include a guarded Windows launcher and real stdio connection probe as installed commands.
- Publish a full capability map, tool schemas, agent guide and contributor workflow.
- Exclude private session reports, personal paths, product content and runtime data.
- Retain 42 workflow tools and historical reference for 94 discovered viewer operations.

The refactored launcher and expanded importer readback require live validation for this release. Prior integration evidence is described separately in docs/VALIDATION.md.
