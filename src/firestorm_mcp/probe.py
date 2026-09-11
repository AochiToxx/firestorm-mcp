"""Probe the existing bridge through a new stdio MCP client; never launch the viewer.

No lease is acquired or released. Exit 0 means connected, 2 means the MCP server
works but the viewer bridge is disconnected, and 1 means the probe itself failed.
"""
from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

from mcp import Client, StdioServerParameters
from .paths import data_root, viewer_directory


def unpack(result):
    if result.is_error:
        raise RuntimeError("; ".join(part.text for part in result.content if part.type == "text"))
    return json.loads(next(part.text for part in result.content if part.type == "text"))


async def probe(root, viewer_dir=None, tool_profile="all"):
    params = StdioServerParameters(command=sys.executable,
        args=["-m", "firestorm_mcp.server", "--data-dir", str(root), "--viewer-dir", str(viewer_dir or viewer_directory()),
              "--tool-profile", tool_profile])
    async with Client(params) as session:
        status = unpack(await session.call_tool("connection_status", {}))
        capabilities = None
        if status.get("connected"):
            capabilities = unpack(await session.call_tool("capabilities_refresh", {}))
        listed = await session.list_tools()
        return {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
                    "entry_point": "MCP stdio client", "mcp_initialized": True,
                    "server": session.server_info.model_dump(by_alias=True), "connection": status,
                    "protocol_version": session.protocol_version, "tool_profile": tool_profile,
                    "tool_count": len(listed.tools),
                    "tool_names": sorted(item.name for item in listed.tools),
                    "capabilities": capabilities, "viewer_started": False,
                    "viewer_input_sent": False, "lease_acquired": False,
                    "lease_owner_verified": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", "--root", dest="root", type=Path, default=data_root())
    parser.add_argument("--viewer-dir", type=Path, default=viewer_directory())
    parser.add_argument("--tool-profile", choices=("all", "compact"), default="all")
    parser.add_argument("--output", type=Path, help="Optional JSON report path; contains no bridge token")
    args = parser.parse_args()
    try:
        report = asyncio.run(asyncio.wait_for(probe(args.root.resolve(), args.viewer_dir, args.tool_profile), timeout=90))
        code = 0 if report["connection"].get("connected") else 2
    except Exception as exc:
        report = {"mcp_initialized": False, "error": type(exc).__name__ + ": " + str(exc)}
        code = 1
    rendered = json.dumps(report, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
