# Agent instructions for Firestorm MCP

This repository is a general-purpose MCP for the Firestorm viewer. Read README.md, docs/AGENT_GUIDE.md and CONTRIBUTING.md before implementing a workflow.

- Source is under src/firestorm_mcp. Keep consumer assets, accounts, simulation rules and product acceptance outside this repository.
- Never modify an active consumer installation as a side effect of development. Use an isolated checkout and FIRESTORM_MCP_HOME pointing to a temporary directory for tests.
- Automated tests must not launch or connect to a live viewer. Real viewer tests require explicit task authority and a bounded control lease; release in cleanup. Never remove another process's lock or kill it to gain control.
- Do not treat tool availability as authority to spend money, send messages, modify inventory/world objects or change shared configuration.
- Preserve source metadata, UI readback, local preview and simulator evidence as different outcomes. A timeout does not cancel a sent action. Unknown fields stay unknown.
- Discover live APIs before unfamiliar calls. Scope UI queries narrowly. Confirm visibility and focus before sending input; re-inspect after human interaction.
- Keep credentials, runtime files, private paths/IDs, captures, logs and product content out of commits and release packages. Do not add telemetry by default.
- Update docs, tool schemas and focused tests alongside API changes. Run pytest with temporary state; exercise a built wheel offline before release.
- Agents may propose contributions through pull requests. The repository owner and maintainers control merging, publishing, access and licence decisions.
