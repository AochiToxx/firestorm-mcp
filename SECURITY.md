# Security

Firestorm MCP gives trusted local software access to your viewer. The bridge binds to loopback, requires a session token and rejects browser Origin requests. It bypasses proxies and refuses redirects. Do not expose its internal `/rpc` endpoint publicly or through a tunnel.

Same-user processes can read the local connection file. Leases coordinate clients but do not block human input. Generic tools do not enforce a universal no-spend policy.

## Report a vulnerability

Use GitHub **Security → Report a vulnerability** when available. Otherwise, request a private reporting channel in an issue without including exploit details or sensitive data.

Include the package version, affected boundary, impact and a small synthetic reproduction. Exclude tokens, private paths, account identifiers and unreviewed logs/captures.

CI checks dependencies against published advisories. A passing scan covers known advisories at that time, not undiscovered vulnerabilities. Only the current alpha line is maintained; no response SLA is promised.
