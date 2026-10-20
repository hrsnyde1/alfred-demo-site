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
        # Hex colours appear only where a design token is defined (for example a
        # dark-mode token block); every other rule uses var(--token).
        for declaration in re.findall(r"([^{};]+):([^{};]+);", css):
            prop, value = (part.strip() for part in declaration)
            if re.search(r"#[0-9a-fA-F]{3,8}\b", value):
                self.assertTrue(prop.startswith("--"), f"hard-coded colour in {prop}")

    def test_footer_reads_hello_from_alfred(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        footer = re.search(r'<footer class="site-footer">(.*?)</footer>', html, re.S)
        self.assertIsNotNone(footer)
        self.assertEqual(re.sub(r"<[^>]+>", "", footer.group(1)).strip(), "hello from Alfred")
        self.assertNotIn("Built by Alfred", html)
        self.assertNotIn("Alfred is Goated", html)
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        rules = re.findall(r"\.site-footer\s*\{(.*?)\}", css, re.S)
        footer_css = "".join(rules)
        self.assertRegex(footer_css, r"font-weight:\s*700;")
        self.assertRegex(footer_css, r"font-size:\s*28px;")
        self.assertIn("color: var(--footer-text)", footer_css)


if __name__ == "__main__":
    unittest.main()
