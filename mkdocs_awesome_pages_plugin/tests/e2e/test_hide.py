from mkdocs_awesome_pages_plugin.navigation import HideInRootHasNoEffect

from .base import E2ETestCase


class TestHide(E2ETestCase):
    def test(self):
        navigation = self.mkdocs(self.config, [("a", ["1.md", self.pagesFile(hide=True)]), ("b", ["2.md"])])

        self.assertEqual(navigation, [("B", [("2", "/b/2")])])

    def test_single_root_section(self):
        navigation = self.mkdocs(self.config, [("section", ["page.md", self.pagesFile(hide=True)])])

        self.assertEqual(navigation, [])

    def test_propagate(self):
        navigation = self.mkdocs(self.config, [("a", [("b", ["page.md", self.pagesFile(hide=True)])])])

        self.assertEqual(navigation, [])

    def test_propagate_deep(self):
        navigation = self.mkdocs(
            self.config,
            [
                (
                    "a",
                    [
                        ("b", [("c", ["1.md", self.pagesFile(hide=True)])]),
                        ("d", ["2.md"]),
                    ],
                )
            ],
        )

        self.assertEqual(navigation, [("A", [("D", [("2", "/a/d/2")])])])

    def test_in_root(self):
        with self.assertWarns(HideInRootHasNoEffect):
            navigation = self.mkdocs(self.config, ["page.md", self.pagesFile(hide=True)])

        self.assertEqual(navigation, [("Page", "/page")])
