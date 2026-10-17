"""Local preview: serves the site and runs api/*.py the way Vercel would.

    python3 serve.py            # http://127.0.0.1:8080
    python3 serve.py --port 9000

Standard library only. Binds to 127.0.0.1, so it is reachable from this machine
only. Static files come from this folder; /api/<name> runs api/<name>.py's handler.
"""

import argparse
import importlib.util
import re
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
API = re.compile(r"/api/([a-z][a-z0-9_-]*)/?(?:\?.*)?\Z")
HIDDEN = (".git", "tests", "__pycache__", "serve.py")


def api_handler(name: str):
    """The `handler` class of api/<name>.py, or None when there is no such function."""
    path = ROOT / "api" / f"{name}.py"
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location(f"api_{name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "handler", None)


class Preview(SimpleHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 (http.server naming)
        match = API.match(self.path)
        if match:
            handler = api_handler(match.group(1))
            if handler is None:
                self.send_error(404, "No such API function")
                return
            # Run the function's own do_GET on this connection.
            handler.do_GET(self)
            return
        if any(part in HIDDEN for part in Path(self.path.split("?", 1)[0]).parts):
            self.send_error(404)
            return
        super().do_GET()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), partial(Preview, directory=str(ROOT)))
    print(f"Preview at http://127.0.0.1:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
