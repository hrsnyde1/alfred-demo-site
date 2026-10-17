"""The local preview server: pages, the API function and hidden paths."""

import importlib.util
import json
import threading
import unittest
import urllib.error
import urllib.request
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("serve", ROOT / "serve.py")
serve = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(serve)


class ServeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(
            ("127.0.0.1", 0), partial(serve.Preview, directory=str(ROOT)))
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def get(self, path):
        with urllib.request.urlopen(self.base + path, timeout=5) as response:
            return response.status, response.headers, response.read()

    def status(self, path):
        try:
            return self.get(path)[0]
        except urllib.error.HTTPError as error:
            return error.code

    def test_serves_the_page(self):
        status, headers, body = self.get("/")
        self.assertEqual(status, 200)
        self.assertIn(b"Harbor &amp; Pine", body)

    def test_runs_the_api_function(self):
        status, headers, body = self.get("/api/tip")
        self.assertEqual(status, 200)
        self.assertIn("tip", json.loads(body))

    def test_unknown_api_and_hidden_paths_are_404(self):
        for path in ("/api/missing", "/api/../serve", "/tests/test_site.py", "/serve.py",
                     "/.git/config"):
            with self.subTest(path=path):
                self.assertEqual(self.status(path), 404)


if __name__ == "__main__":
    unittest.main()
