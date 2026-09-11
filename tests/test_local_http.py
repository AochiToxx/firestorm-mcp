import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

from firestorm_mcp.bridge import make_handler


class StubBridge:
    def handle(self, request):
        return {"connected": True}


def test_loopback_auth_origin_and_valid_request():
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(StubBridge(), "test-secret"))
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
        with opener.open(urllib.request.Request(url, b'{}', {"Authorization": "Bearer test-secret"}), timeout=2) as response:
            assert json.load(response)["result"]["connected"]
    finally:
        server.shutdown()
        server.server_close()
        thread.join(2)
