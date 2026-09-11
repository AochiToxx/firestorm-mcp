# Security reporting and operating boundary

This alpha grants powerful access to a local viewer. Use it only with an MCP host and local software you trust. The HTTP bridge binds to loopback, requires a per-session token and rejects browser Origin requests. Same-user processes can read its local connection file; this is not isolation from other software running as that user. Do not expose the endpoint through a tunnel or public web server.

Use GitHub **Security → Report a vulnerability** when private vulnerability reporting is available. If that option is unavailable, ask for a private reporting channel in a minimal issue containing no exploit details, tokens, logs or personal data. Do not place credentials or private captures in public issues.

Reports should identify the version, affected boundary, a minimal synthetic reproduction and impact. Redact machine/account paths and identifiers. The maintainers do not promise a response SLA. Only the current alpha line is maintained; known limitations are documented in the README.

Generic UI and viewer APIs can perform consequential actions. Leases coordinate cooperating clients and do not lock out human input. Never treat the MCP as a universal no-spend or transaction-approval enforcement system.
