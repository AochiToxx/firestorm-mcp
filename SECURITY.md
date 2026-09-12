# Security

Firestorm MCP gives trusted local software access to your viewer. The bridge binds to loopback, requires a session token and rejects browser Origin requests. It bypasses proxies and refuses redirects. Do not expose its internal `/rpc` endpoint publicly or through a tunnel.

Same-user processes can read the local connection file. Leases coordinate clients but do not block human input. Generic tools do not enforce a universal no-spend policy.

## Report a vulnerability

Use [Report a vulnerability](https://github.com/AochiToxx/firestorm-mcp/security/advisories/new) to contact maintainers privately. Do not post exploit details or sensitive data in a public issue.

Include the package version, affected boundary, impact and a small synthetic reproduction. Exclude tokens, private paths, account identifiers and unreviewed logs/captures.

Only the current alpha line is maintained; no response SLA is promised.

## Repository protections

The upstream GitHub repository uses protected pull requests, CodeQL, secret scanning, push protection and Dependabot alerts. CI also checks dependencies against published advisories. These checks have limited coverage; passing them does not prove code is safe.

External workflow runs require maintainer approval. Release tags are protected, and newly published releases are immutable. [CONTRIBUTING.md](CONTRIBUTING.md) explains the review and release workflow. Repository settings are managed on GitHub; cloning the source does not configure them for your own repository.
