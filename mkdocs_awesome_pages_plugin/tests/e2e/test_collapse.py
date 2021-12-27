from .base import E2ETestCase


class TestCollapseGlobalDisabled(E2ETestCase):
    def test_no_collapse(self):
        navigation = self.mkdocs(self.config, [("section", ["page.md"])])

        self.assertEqual(navigation, [("Section", [("Page", "/section/page")])])

    def test_local(self):
        navigation = self.mkdocs(
            self.config,
            [("a", [("b", [("c", ["page.md"]), self.pagesFile(collapse=True)])])],
        )

        self.assertEqual(navigation, [("A", [("C", [("Page", "/a/b/c/page")])])])

    def test_local_recursively(self):
        navigation = self.mkdocs(
            self.config,
            [
                (
                    "a",
                    [
                        (
                            "b",
                            [
                                ("c", ["page.md"]),
                                self.pagesFile(collapse_single_pages=True),
                            ],
                        )
                    ],
                )
            ],
        )

        self.assertEqual(navigation, [("A", [("Page", "/a/b/c/page")])])

    def test_local_recursively_except_current(self):
        navigation = self.mkdocs(
            self.config,
            [
                (
                    "a",
                    [
                        (
                            "b",
                            [
                                ("c", ["page.md"]),
                                self.pagesFile(collapse_single_pages=True, collapse=False),
                            ],
                        )
                    ],
                )
            ],
        )

        self.assertEqual(navigation, [("A", [("B", [("Page", "/a/b/c/page")])])])

    def test_local_with_hide(self):
        navigation = self.mkdocs(
            self.config,
            [
                (
                    "a",
                    [
                        (
                            "b",
                            [
                                ("c", ["1.md"]),
                                ("d", ["2.md", self.pagesFile(hide=True)]),
                                self.pagesFile(collapse=True),
                            ],
                        )
                    ],
                )
            ],
        )

        self.assertEqual(navigation, [("A", [("C", [("1", "/a/b/c/1")])])])


class TestCollapseGlobalEnabled(E2ETestCase):
    def setUp(self):
        self.config = self.createConfig(collapse_single_pages=True)

    def test(self):
        navigation = self.mkdocs(self.config, [("section", ["page.md"])])

        self.assertEqual(navigation, [("Page", "/section/page")])

    def test_deep(self):
        navigation = self.mkdocs(self.config, [("a", [("b", [("c", ["page.md"])])])])

        self.assertEqual(navigation, [("Page", "/a/b/c/page")])

    def test_override_local(self):
        navigation = self.mkdocs(
            self.config,
            [("a", [("b", [("c", ["page.md"]), self.pagesFile(collapse=False)])])],
        )

        self.assertEqual(navigation, [("B", [("Page", "/a/b/c/page")])])

    def test_override_local_recursively(self):
        navigation = self.mkdocs(
            self.config,
            [
                (
                    "a",
                    [
                        (
                            "b",
                            [
                                ("c", ["page.md"]),
                                self.pagesFile(collapse_single_pages=False),
                            ],
                        )
                    ],
                )
            ],
        )

        self.assertEqual(navigation, [("B", [("C", [("Page", "/a/b/c/page")])])])

    def test_title(self):
        navigation = self.mkdocs(
            self.config,
            [("section", ["page.md", self.pagesFile(title="Section Title")])],
        )

        self.assertEqual(navigation, [("Page", "/section/page")])

    def test_links(self):
        navigation = self.mkdocs(
            self.createConfig(
                mkdocs_nav=[
                    {
                        "Section": [
                            {"Page": "section/page.md"},
                            {"Link": "https://example.com"},
                        ]
                    }
                ]
            ),
            [("section", ["page.md"])],
        )

        self.assertEqual(
            navigation,
            [("Section", [("Page", "/section/page"), ("Link", "https://example.com")])],
        )

    def test_arrange_duplicate(self):
        navigation = self.mkdocs(
            self.createConfig(
                mkdocs_nav=[
                    {
                        "Section": [
                            {"Page": "section/page.md"},
                            {"Page": "section/page.md"},
                        ]
                    }
                ]
            ),
            [("section", ["page.md"])],
        )

        self.assertEqual(
            navigation,
            [("Section", [("Page", "/section/page"), ("Page", "/section/page")])],
        )

    def test_local_with_hide(self):
        navigation = self.mkdocs(
            self.config,
            [
                (
                    "a",
                    [
                        (
                            "b",
                            [
                                ("c", ["1.md"]),
                                ("d", ["2.md", self.pagesFile(hide=True)]),
                            ],
                        )
                    ],
                )
            ],
        )

        self.assertEqual(navigation, [("1", "/a/b/c/1")])
