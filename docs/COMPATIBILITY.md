# MCP compatibility and ecosystem audit

Reviewed 11 September 2026. The audit compared `0.2.0a1` with the **`0.3.0a1` private baseline**. It combines primary-source research, code inspection, isolated tests and a coordinated live consumer test. It is not a certification by the MCP project, a penetration test or a promise that every agent application has been exercised.

## Main findings and disposition

| Finding in the release | Impact | Development change / remaining work |
| --- | --- | --- |
| `mcp>=1.12,<2` restricts the server to the older SDK/protocol family | A client requiring the current revision cannot use its new discovery flow | Migrated to `mcp>=2.2,<3`; raw stdio tests cover `2024-11-05`, `2025-03-26`, `2025-06-18`, `2025-11-25` and `2026-07-28` |
| The historical expanded catalog has 136 tools | Exceeds some host/request limits before another MCP is added | Added `--tool-profile compact`: 43 workflow tools, with every discovered operation still reachable through `viewer_call`; default `all` preserves individual operations after refresh |
| Catalog-change notifications were sent but not advertised | Hosts may keep a stale tool list after login/discovery | Advertise legacy changes and implement the current subscription path with the SDK; notify only when definitions change |
| Viewer discovery ran before MCP startup | A slow bridge could consume the host's startup timeout | Server discovery and tool listing now start without contacting a viewer; refresh is explicit |
| Results were JSON text/images only | Clients had to parse text to consume machine-readable data | Added `structuredContent`, preserving JSON text and PNG blocks; non-object results use a `result` wrapper only in structured data |
| Unknown/extra fields and arbitrary names had weak handling | Silent typos or an unknown tool could cause unwanted discovery | Validate advertised JSON schemas before dispatch, forbid extra workflow arguments and return a protocol error for unknown tools |
| Read-only and open-world hints were conflated | A host could misclassify a viewer read as confined to local data | Viewer tools retain open-world hints; local file tools are distinguished; image comparison is marked as writing a file |
| Setup documentation treated host wrappers generically | Users can paste valid JSON into the wrong host schema | Added separate Windows examples for Codex, Claude Desktop, Claude Code, Cursor and VS Code; distinguish local desktop from remote/WSL/container execution |
| A new virtual environment inherited an old pip with published advisories | Installer tooling can lag behind current archive-extraction fixes | Installer updates only its dedicated pip to `>=26.2,<27`; the isolated environment was updated to 26.2.1 and its repeat advisory scan reported no known vulnerabilities |
| UI search matched the whole path and silently capped results | Relevant tabs could be buried behind hundreds of hidden descendants | Added basename, exact, prefix, glob and depth filters, sorted pages, explicit next offset and truncation |
| Mouse handling was mistaken for button/selection effects | A tab or combo could remain unchanged after a handled input | Added registered button callbacks with unique-path guards; keys require an explicit visible/enabled target and return before/after state |
| Valid PNG files could be completely black | Agents could count unusable captures as scene evidence | Added flat/black/transparent image flags; nonblank content still requires visual review |
| Local endpoint validation did not prevent redirects | A redirected request could leave the intended local route | Client now refuses all redirects; regression tests exercise 301/302/303/307/308 |
| Rejected small HTTP bodies could reset a Windows connection | A caller could receive a socket error instead of the intended authorization error | Drain bounded small rejected bodies with a one-second read timeout; never parse or dispatch rejected input |
| Some paths returned by the viewer could not be inspected individually | One invalid child path aborted an otherwise useful UI search page | Preserve the page and attach an explicit per-item inspection error |
| The uploader preview could be too small for useful comparison | A nonblank capture still lacked enough detail to inspect LODs | Added bounded path-targeted uploader zoom/pan/orbit input; callers must inspect fresh captures because camera pose is not observable |

The MCP specification now names **2026-07-28** as current. Its discovery and request versioning differ from the previous handshake model. The official Python SDK v2 implements both eras; SDK v1 is maintained separately for critical fixes. The migration follows that SDK rather than implementing a custom protocol dialect. Sources: [MCP versioning](https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning), [revision changes](https://modelcontextprotocol.io/specification/2026-07-28/changelog), [SDK migration guide](https://py.sdk.modelcontextprotocol.io/migration/).

The tool-count issue is a host constraint, not an MCP-wide maximum. VS Code documents 128 tools per request and offers selection/virtual-tool controls. Other tools in the same agent count toward that budget. Source: [VS Code tools](https://code.visualstudio.com/docs/agents/run/tools).

## Projects compared

| Primary project | Relevant pattern | Decision for Firestorm MCP |
| --- | --- | --- |
| [Blender MCP](https://github.com/ahujasid/blender-mcp) | Separate application connection and MCP server, multiple client setup guides and versioned package installation | Keep the visible viewer/LEAP boundary, document host configuration and diagnostics; do not add unrelated asset-provider services |
| [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp) | Semantic tools and optional capability groups, with configuration for host/session differences | Add a compact presentation and retain explicit state readback; use stable viewer semantics where available instead of treating a click acknowledgment as success |
| [MikoStorm](https://github.com/DDynamic-Evolution/MikoStorm) | A custom viewer with built-in HTTP MCP, named viewer tools and state resources | Useful feature comparison; our package continues to use an installed standard Firestorm viewer. We did not install/test MikoStorm or copy its C++ implementation |
| [Official reference servers](https://github.com/modelcontextprotocol/servers) | Examples of distinct tools, resources and prompts, each scoped to a purpose | Do not add optional protocol features merely to increase the feature count |
| [Official MCP Inspector](https://github.com/modelcontextprotocol/inspector) | Independent client and schema inspection, CLI suitable for repeatable checks | Added a pinned, offline Inspector check using version 2.6.0; this complements raw-wire and Python-client tests |
| [MCP Bundles](https://github.com/modelcontextprotocol/mcpb) | Host-managed local extension installation; Python/UV bundle formats | Candidate for a later Windows install package after clean-machine tests, not an existing downloadable feature |

## Compatibility evidence

| Surface | Evidence / support boundary |
| --- | --- |
| Raw JSON-RPC over stdio | Five protocol revisions exercised directly, independent of Python client wrappers: startup/discovery, sorted tool listing, errors, asset metadata, UTF-8 paths and PNG content |
| Official Python SDK v2 | Real subprocess connection and offline tool calls; current protocol discovery supported |
| Legacy/current dynamic discovery | Mock viewer changes the catalog; old-style notification and current `subscriptions/listen` delivery tested; dynamic argument rejection occurs before mock dispatch |
| Compact profile | Mock viewer refresh leaves 43 listed tools; generic operation call succeeds; it is a presentation option, not a permissions sandbox |
| Official Inspector | `scripts/verify_inspector.py` runs strict discovery and a disconnected-status call in temporary state; requires Node >=22.19.0 |
| Codex | Coordinated candidate cutover and real SDK-v2 stdio workflow from a Codex task; native tool refresh/application UI acceptance is separate |
| Claude Desktop / Claude Code / Cursor / VS Code | Official configuration formats researched and documented; application UI acceptance not yet run |
| Windows/Python | CI matrix covers 3.11/3.12/3.13/3.14. Platform-independent wheel filename does not certify non-Windows viewer control |
| Remote/cloud/WSL/container-only hosts | No direct support for native desktop control; no public MCP HTTP endpoint is implemented |

See [VALIDATION.md](VALIDATION.md) for executed checks and [INSTALLATION.md](INSTALLATION.md) for exact host configuration. Passing a simulated importer test does not verify a live viewer or a Second Life upload.

## Required before broader release claims

1. **Repeat the coordinated consumer test for future upgrades.** The wheel-installed candidate launcher/helper, signed-in state, compact discovery and consumer importer workflow have been live-checked for this baseline. The observations and untested cases are recorded in [VALIDATION.md](VALIDATION.md). Do not mutate an active installation as a build side effect.
2. **Test actual host applications.** Complete a small matrix for Claude Desktop, Claude Code, Cursor and VS Code on Windows. Record application/version, connection, tool listing, discovery refresh, structured/image output and error handling. Protocol compatibility alone is not application certification.
3. **Extend viewer evidence coverage.** Precise search, registered button callbacks, path-targeted keys and blank-image detection are implemented with regression tests. Confirm behavior for each additional viewer build. Human interaction, shortcut handling, stale images and hidden UI values still require inspection; a nonblank frame or successful callback does not prove the requested effect.
4. **Bound long operations more clearly.** Orbit capture and multi-control readback can exceed a host's default timeout. Calls are serialized, viewer RPCs are bounded, and a cancelled queued request is tested not to reach the viewer. Progress reporting, workflow deadlines and more cancellation/fault scenarios remain useful work. Never equate an MCP cancellation with undoing an already dispatched viewer action.
5. **Harden distribution and permissions before a remote service.** The local bridge uses a random bearer token, loopback-only address validation, proxy bypass, redirect refusal, Origin rejection and bounded bodies. It trusts the local user's filesystem and allowed callers. It is not a multi-tenant service, a general filesystem sandbox or a server-side policy engine for paid/chat/inventory operations. Adding HTTP/tunneling requires a deliberate authentication, session-isolation and authorization design.

## Optional features, not missing protocol requirements

- **Resources and prompts:** convenient future additions for a static agent guide or explicit state reads. Tools-only servers are valid; advertise only implemented features. Do not expose private chat/inventory/captures as resources by default. [MCP capability negotiation](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle).
- **Sampling, elicitation and tasks:** unnecessary for the present local viewer workflow. Do not require host-side model calls or user-input round trips just to connect. Evaluate long-running task support when there is a concrete cancellable operation.
- **HTTP transport / OAuth:** needed for a deliberately designed remote product, not this local stdio package. The bridge's `/rpc` endpoint is not an MCP server URL. [MCP transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports).
- **One-click `.mcpb` installation:** promising, especially a host-managed UV environment, but host support, Python/native dependencies and the viewer launcher need clean Windows testing. Do not bundle a developer's virtual environment or the viewer. [MCP bundle formats](https://github.com/modelcontextprotocol/mcpb).
- **PyPI, `uvx` and official Registry:** improve public discovery/install once publication is approved. A PyPI-based listing needs a published package, ownership marker and validated `server.json`; neither a private GitHub ZIP nor an invented `uvx firestorm-mcp` command establishes availability. [Registry package requirements](https://modelcontextprotocol.io/registry/package-types).
- **Supply-chain improvements:** CI now runs dependency advisory checks. Review dependency updates and consider signed/attested build artifacts. Checksums detect differences from a release; they are not publisher identity verification.

## License scope

MIT is a common MCP ecosystem choice: the [official Python SDK](https://github.com/modelcontextprotocol/python-sdk/blob/main/LICENSE) and [Blender MCP](https://github.com/ahujasid/blender-mcp/blob/main/LICENSE) use it. It is not an MCP requirement: [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp/blob/main/LICENSE) uses Apache-2.0. The protocol and the implementation's software license are separate choices.

This repository's MIT license permits use, modification and redistribution, including commercial redistribution, provided recipients retain the copyright and permission notice. It does not require modifications to be published. The disclaimer provides the software without a warranty. Private repository access is a separate GitHub setting; someone who receives MIT-licensed code obtains its license permissions, so private access should not be mistaken for a redistribution restriction. Dependencies keep their own licenses, and the Firestorm viewer is distributed separately. [Official MIT text](https://opensource.org/license/mit), [project attribution inventory](../THIRD_PARTY.md).
