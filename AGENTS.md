# Agent instructions

Read [README.md](README.md), [AGENT_GUIDE.md](docs/AGENT_GUIDE.md) and [CONTRIBUTING.md](CONTRIBUTING.md) before changing a workflow.

1. **Keep the integration general.** Source is in `src/firestorm_mcp`. Keep consumer assets, accounts, business rules and product signoff outside this repository.
2. **Isolate development.** Use a separate environment and temporary `FIRESTORM_MCP_HOME`. Automated tests must not launch/contact a live viewer or modify an active installation.
3. **Respect control ownership.** Live tests require task authority and a bounded lease, released in cleanup. Never remove another process's lock or kill it to gain access. Tool availability does not authorize spending, chat or inventory/world changes.
4. **Verify effects.** Discover live APIs, scope UI queries and check visibility/focus before input. Reinspect after human interaction. Keep source metadata, UI readback, local preview and simulator evidence distinct. A timeout does not cancel a sent action; unknown values stay unknown.
5. **Keep releases reviewable.** Exclude credentials, private paths/IDs, captures, logs and product content. Add no default telemetry. Update affected docs/schemas and run focused tests; package changes need an offline wheel check. Use a branch and PR; never weaken checks to merge. Maintainers control merging, releases and access.
