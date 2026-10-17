"""The page's structure and the stylesheet's design tokens. Standard library only."""

import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags, self.ids, self.links, self.scripts = [], set(), [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.links.append(attrs.get("href"))
        if tag == "script" and attrs.get("src"):
            self.scripts.append(attrs["src"])


def page():
    parser = Page()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    return parser


class SiteTest(unittest.TestCase):
    def test_page_has_landmarks(self):
        tags = page().tags
        for landmark in ("header", "nav", "main", "footer"):
            self.assertIn(landmark, tags)

    def test_page_loads_its_stylesheet_and_script(self):
        parsed = page()
        self.assertEqual(parsed.links, ["styles.css"])
        self.assertEqual(parsed.scripts, ["app.js"])
        self.assertTrue((ROOT / "styles.css").is_file())
        self.assertTrue((ROOT / "app.js").is_file())

    def test_navigation_targets_exist(self):
        ids = page().ids
        for target in ("services", "work", "contact", "tip"):
            self.assertIn(target, ids)

    def test_colours_come_from_design_tokens(self):
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        root = re.search(r":root\s*\{(.*?)\}", css, re.S)
        self.assertIsNotNone(root)
        for token in ("--background", "--surface", "--text", "--muted", "--accent"):
            self.assertIn(token, root.group(1))
        # Outside :root, colours are referenced through tokens, not hard-coded.
        rest = css[root.end():]
        self.assertEqual(re.findall(r"#[0-9a-fA-F]{3,8}\b", rest), [])


if __name__ == "__main__":
    unittest.main()
