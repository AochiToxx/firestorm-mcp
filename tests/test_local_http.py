import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

import pytest

from firestorm_mcp.bridge import make_handler
from firestorm_mcp.client import BridgeClient


class StubBridge:
    def __init__(self):
        self.requests = []

    def handle(self, request):
        self.requests.append(request)
        return {"connected": True}


def test_loopback_auth_origin_and_valid_request():
    bridge = StubBridge()
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(bridge, "test-secret"))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    url = f"http://127.0.0.1:{server.server_port}/rpc"
    try:
        for headers, expected in [({}, 401), ({"Authorization": "Bearer wrong"}, 401),
                                  ({"Authorization": "Bearer test-secret", "Origin": "https://example.com"}, 403)]:
            with pytest.raises(urllib.error.HTTPError) as caught:
                opener.open(urllib.request.Request(url, b'{}', headers), timeout=2)
            assert caught.value.code == expected
        assert bridge.requests == []  # Rejected bodies never reach the dispatcher.
        with opener.open(urllib.request.Request(url, b'{}', {"Authorization": "Bearer test-secret"}), timeout=2) as response:
            assert json.load(response)["result"]["connected"]
        assert bridge.requests == [{}]
    finally:
        server.shutdown()
        server.server_close()
        thread.join(2)


@pytest.mark.parametrize("status", [301, 302, 303, 307, 308])
def test_client_never_follows_redirects(tmp_path, status):
    forwarded = []
    class Redirect(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass
        def do_POST(self):
            self.rfile.read(int(self.headers.get("Content-Length", "0")))
            self.send_response(status)
            self.send_header("Location", f"http://127.0.0.1:{self.server.server_port}/other")
            self.end_headers()
        def do_GET(self):
            forwarded.append(self.headers.get("Authorization"))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"result": {}}')
    server = ThreadingHTTPServer(("127.0.0.1", 0), Redirect)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    (tmp_path / "connection.json").write_text(json.dumps({
        "url": f"http://127.0.0.1:{server.server_port}/rpc", "token": "synthetic-only"}))
    try:
        with pytest.raises(ConnectionError, match="Bridge HTTP error"):
            BridgeClient(tmp_path).rpc("status")
        assert not forwarded
    finally:
        server.shutdown()
        server.server_close()
        thread.join(2)
