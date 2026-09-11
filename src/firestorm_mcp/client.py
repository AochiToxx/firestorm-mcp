from __future__ import annotations

import json
from pathlib import Path
import urllib.error
import urllib.request
import urllib.parse
import uuid


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # A local response must never forward the bearer token or action elsewhere.
        return None


class BridgeClient:
    def __init__(self, runtime: Path):
        self.runtime = Path(runtime)
        self.client_id = uuid.uuid4().hex
        self.apis = {}

    def rpc(self, method, **arguments):
        try:
            connection = json.loads((self.runtime / "connection.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            raise ConnectionError("Firestorm bridge connection metadata is unavailable. Check viewer/bridge state before coordinating a launcher start.") from None
        endpoint = urllib.parse.urlsplit(connection["url"])
        if (endpoint.scheme != "http" or endpoint.hostname != "127.0.0.1" or endpoint.username is not None
                or endpoint.password is not None or endpoint.path != "/rpc" or endpoint.query or endpoint.fragment):
            raise ValueError("Bridge endpoint must be loopback")
        request = urllib.request.Request(connection["url"],
            json.dumps({"method": method, "client_id": self.client_id, **arguments}, allow_nan=False).encode("utf-8"),
            {"Content-Type": "application/json", "Authorization": "Bearer " + connection["token"]})
        try:
            # Explicitly bypass system proxies for this local-only connection.
            with urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect()).open(request, timeout=70) as response:
                result = json.load(response)
        except urllib.error.HTTPError as exc:
            try:
                error = json.load(exc)["error"]
                raise RuntimeError(error["type"] + ": " + error["message"]) from None
            except (ValueError, KeyError):
                raise ConnectionError(f"Bridge HTTP error {exc.code}") from None
        except urllib.error.URLError as exc:
            raise ConnectionError("Firestorm bridge is unavailable at the recorded endpoint. Check viewer/bridge state; do not restart a shared session solely for tool discovery.") from exc
        if method == "discover":
            self.apis = result["result"]
        return result["result"]

    def call(self, api, op, arguments=None, **kwargs):
        if kwargs.get("expect_reply") is None:
            if api not in self.apis:
                self.rpc("discover")
            descriptor = next((item for item in self.apis.get(api, {}).get("ops", []) if item["name"] == op), {})
            kwargs["expect_reply"] = ("reply" in (descriptor.get("required") or {}) or
                                      '"reply"' in descriptor.get("desc", "") or
                                      (api == "LLFloaterReg" and op == "clickButton"))
        return self.rpc("call", api=api, op=op, arguments=arguments or {}, **kwargs)
