from ...navigation import TitleInRootHasNoEffect
from .base import E2ETestCase


class TestPageTitle(E2ETestCase):
    # With MkDocs v1 this feature is implemented by MkDocs itself.
    # This test only exists to test feature parity with MkDocs v0.
    def test_h1_from_markdown(self):
        navigation = self.mkdocs(self.config, [("page.md", "# Page Title")])

        self.assertEqual(navigation, [("Page Title", "/page")])


class TestSectionTitle(E2ETestCase):
    def test(self):
        navigation = self.mkdocs(
            self.config,
            [("section", ["page.md", self.pagesFile(title="Section Title")])],
        )

        self.assertEqual(navigation, [("Section Title", [("Page", "/section/page")])])

    def test_in_root(self):
        with self.assertWarns(TitleInRootHasNoEffect):
            navigation = self.mkdocs(self.config, ["page.md", self.pagesFile(title="Root Title")])

        self.assertEqual(navigation, [("Page", "/page")])

    def test_deep(self):
        navigation = self.mkdocs(
            self.config,
            [
                (
                    "a",
                    [
                        ("b", ["page.md", self.pagesFile(title="Section B Title")]),
                        self.pagesFile(title="Section A Title"),
                    ],
                )
            ],
        )

        self.assertEqual(
            navigation,
            [("Section A Title", [("Section B Title", [("Page", "/a/b/page")])])],
        )

    def test_title_in_nav(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"Nav Title": [{"Page": "section/page.md"}]}]),
            [("section", ["page.md", self.pagesFile(title="Section Title")])],
        )

        self.assertEqual(navigation, [("Nav Title", [("Page", "/section/page")])])
