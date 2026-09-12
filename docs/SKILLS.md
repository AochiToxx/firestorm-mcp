# Optional agent workflow skill

**MCP runtime:** 0.3.0a1. **Skill:** `firestorm-mesh-preview` 0.1.0.

The MCP provides callable viewer tools. The skill gives an agent a concise entry
point and an on-demand importer procedure for choosing and sequencing those tools.
It follows the open [Agent Skills format](https://agentskills.io/specification).
Skills-compatible hosts can discover its name/description and load its full
instructions when relevant; exact installation and activation depend on the host.
See the [format overview](https://agentskills.io/home).

This is an optional companion to the existing MCP, not a viewer extension or a
new transport. Installing it does not install/register the MCP, add server tools,
change a viewer session or grant permissions. It is intended to reduce repeated
investigation; a speedup has not yet been measured. Skills cannot repair a viewer
API or replace server-side enforcement.

The host can still load MCP tool schemas independently of the skill. Use the
existing compact MCP profile to limit that catalog; installing a skill does not
automatically remove schemas from an agent's context.

## Download and use

1. [Download the skill ZIP](https://github.com/AochiToxx/firestorm-mcp/releases/download/skill-v0.1.0/firestorm-mesh-preview-0.1.0.zip)
   and extract it. Keep the complete `firestorm-mesh-preview` folder together;
   it contains `SKILL.md`, `references/importer.md` and `LICENSE`.
2. Add that folder through your agent host's supported skill import mechanism or
   documented skills directory. A repository folder alone is not automatic
   installation in every host. Existing MCP users do not need a viewer restart
   just to add these instructions.
3. With Firestorm MCP configured, invoke the skill using the host's skill picker
   or supported invocation syntax, and supply your actual export files and check.
   For example: "Use firestorm-mesh-preview to compare my supplied High and Lowest
   exports in the importer. Collect evidence and leave upload for a separate decision."

If the host has no skills loader but can read files, ask it to read the extracted
`SKILL.md` and follow the linked importer reference for the relevant task. That is
manual use of the same instructions, not a claim of native skill integration.

The [source folder](../skills/firestorm-mesh-preview) can also be copied from a
clone; include the repository's `LICENSE` when redistributing it separately.
The standalone ZIP includes that licence automatically. Private release downloads
require repository access. The existing 0.3.0a1 runtime ZIP/wheel predates this
skill, so download the companion separately; do not expect it inside older assets.

## What the skill changes for an agent

- Guides the tested workflow without requiring the full historical API reference.
- Records source selection/commit and checkbox-key procedures that otherwise cost investigation.
- Calls for scoped discovery and targeted observations between full checkpoints.
- Separates filenames, local hashes, displayed quote values and rendered evidence.
- Produces useful bug reports while keeping private product data outside the repository.

The workflow remains driven by the agent through the real MCP. It is not a
single-call five-file import macro. User authority, leases and live state checks
still apply; the instructions are not a sandbox for low-level viewer operations.

## Validation and contribution

The packaged entrypoint and reference use the current tool schemas and preserve
the tested Firestorm 7.2.4.80712 procedures. The skill is format-validated and its
archive has deterministic contents, a bundled MIT licence and a SHA-256 checksum.
An offline consumer review checks the instructions separately from live runtime
evidence. That review does not certify host-specific automatic activation or a
fresh end-to-end skill-driven viewer run.

Improve the skill through a focused pull request under
`skills/firestorm-mesh-preview/`. Include a realistic request, the point where an
agent struggled, and the observed result. Keep reusable procedure changes here;
keep API fixes in the MCP implementation. Use [CONTRIBUTING.md](../CONTRIBUTING.md)
for the repository workflow and [VALIDATION.md](VALIDATION.md) for runtime evidence.

Build the standalone package from a checkout:

```powershell
python scripts/build_skill.py --output-dir dist
```

The builder includes only the two skill documents and the root MIT licence. The
normal source-distribution builder includes the skill sources in future source
packages. The Python wheel remains the MCP runtime, without automatically
installing files into an agent host's personal directories.
