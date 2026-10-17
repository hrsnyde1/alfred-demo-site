"""GET /api/tip — the tip of the day, as JSON. Runs as a Vercel Python function."""

import datetime as dt
import json
from http.server import BaseHTTPRequestHandler

TIPS = (
    "Small, steady improvements beat big rewrites.",
    "Write the headline first; the layout follows.",
    "Every page should answer one question clearly.",
    "Test on a phone before you test on a laptop.",
    "Readable beats clever, in code and in copy.",
    "Fast pages feel friendly.",
    "Ask one real customer before you redesign.",
)


def pick_tip(day: dt.date) -> str:
    """The same tip all day, a different one each day."""
    return TIPS[day.toordinal() % len(TIPS)]


class handler(BaseHTTPRequestHandler):  # noqa: N801 (Vercel requires this name)
    def do_GET(self):  # noqa: N802 (http.server naming)
        body = json.dumps({"tip": pick_tip(dt.date.today())}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "public, max-age=3600")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
