"""The /api/tip function, run in-process without a server. Standard library only."""

import datetime as dt
import importlib.util
import io
import json
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "tip", Path(__file__).resolve().parents[1] / "api" / "tip.py")
tip = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tip)


class FakeRequest(tip.handler):
    """Drives the handler's do_GET without a socket."""

    def __init__(self):
        self.wfile = io.BytesIO()
        self.status, self.headers_out = None, {}

    def send_response(self, code, message=None):
        self.status = code

    def send_header(self, keyword, value):
        self.headers_out[keyword] = value

    def end_headers(self):
        pass


class TipTest(unittest.TestCase):
    def test_same_tip_all_day(self):
        day = dt.date(2026, 10, 17)
        self.assertEqual(tip.pick_tip(day), tip.pick_tip(day))

    def test_tips_rotate_through_the_week(self):
        start = dt.date(2026, 10, 17)
        week = {tip.pick_tip(start + dt.timedelta(days=i)) for i in range(len(tip.TIPS))}
        self.assertEqual(week, set(tip.TIPS))

    def test_get_returns_json(self):
        request = FakeRequest()
        request.do_GET()
        self.assertEqual(request.status, 200)
        self.assertTrue(request.headers_out["Content-Type"].startswith("application/json"))
        body = json.loads(request.wfile.getvalue())
        self.assertIn(body["tip"], tip.TIPS)


if __name__ == "__main__":
    unittest.main()
