from ...navigation import NavEntryNotFound
from .base import E2ETestCase


class TestArrange(E2ETestCase):
    pages123 = ["1.md", "2.md", "3.md"]

    def test(self):
        navigation = self.mkdocs(
            self.config,
            [
                (
                    "section",
                    [*self.pages123, self.pagesFile(arrange=["2.md", "...", "1.md"])],
                )
            ],
        )

        self.assertEqual(
            navigation,
            [
                (
                    "Section",
                    [("2", "/section/2"), ("3", "/section/3"), ("1", "/section/1")],
                )
            ],
        )

    def test_no_config(self):
        navigation = self.mkdocs(
            self.config,
            [
                (
                    "section",
                    [
                        *self.pages123,
                    ],
                )
            ],
        )

        self.assertEqual(
            navigation,
            [
                (
                    "Section",
                    [("1", "/section/1"), ("2", "/section/2"), ("3", "/section/3")],
                )
            ],
        )

    def test_all_in_config(self):
        navigation = self.mkdocs(
            self.config,
            [*self.pages123, self.pagesFile(arrange=["3.md", "1.md", "2.md"])],
        )

        self.assertEqual(navigation, [("3", "/3"), ("1", "/1"), ("2", "/2")])

    def test_some_in_config(self):
        navigation = self.mkdocs(self.config, [*self.pages123, self.pagesFile(arrange=["2.md"])])

        self.assertEqual(navigation, [("2", "/2"), ("1", "/1"), ("3", "/3")])

    def test_rest_start(self):
        navigation = self.mkdocs(self.config, [*self.pages123, self.pagesFile(arrange=["...", "2.md"])])

        self.assertEqual(navigation, [("1", "/1"), ("3", "/3"), ("2", "/2")])

    def test_rest_middle(self):
        navigation = self.mkdocs(
            self.config,
            [*self.pages123, self.pagesFile(arrange=["2.md", "...", "1.md"])],
        )

        self.assertEqual(navigation, [("2", "/2"), ("3", "/3"), ("1", "/1")])

    def test_rest_end(self):
        navigation = self.mkdocs(self.config, [*self.pages123, self.pagesFile(arrange=["2.md", "..."])])

        self.assertEqual(navigation, [("2", "/2"), ("1", "/1"), ("3", "/3")])

    def test_empty_rest(self):
        navigation = self.mkdocs(
            self.config,
            [*self.pages123, self.pagesFile(arrange=["3.md", "2.md", "...", "1.md"])],
        )

        self.assertEqual(navigation, [("3", "/3"), ("2", "/2"), ("1", "/1")])

    def test_only_rest(self):
        navigation = self.mkdocs(self.config, [*self.pages123, self.pagesFile(arrange=["..."])])

        self.assertEqual(navigation, [("1", "/1"), ("2", "/2"), ("3", "/3")])

    def test_sections(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                "2.md",
                ("a", ["3.md", "4.md"]),
                ("b", ["5.md", "6.md"]),
                self.pagesFile(arrange=["a", "...", "2.md"]),
            ],
        )

        self.assertEqual(
            navigation,
            [
                ("A", [("3", "/a/3"), ("4", "/a/4")]),
                ("1", "/1"),
                ("B", [("5", "/b/5"), ("6", "/b/6")]),
                ("2", "/2"),
            ],
        )

    def test_deep(self):
        navigation = self.mkdocs(
            self.config,
            [
                (
                    "a",
                    ["1.md", "2.md", "3.md", self.pagesFile(arrange=["...", "1.md"])],
                ),
                ("b", ["4.md", "5.md", "6.md", self.pagesFile(arrange=["5.md"])]),
                self.pagesFile(arrange=["b", "a"]),
            ],
        )

        self.assertEqual(
            navigation,
            [
                ("B", [("5", "/b/5"), ("4", "/b/4"), ("6", "/b/6")]),
                ("A", [("2", "/a/2"), ("3", "/a/3"), ("1", "/a/1")]),
            ],
        )

    def test_links(self):
        navigation = self.mkdocs(
            self.createConfig(
                mkdocs_nav=[
                    {"Link 1": "https://example.com"},
                    {"Page 1": "1.md"},
                    {"Link 2": "https://example.com"},
                    {"Page 2": "2.md"},
                ]
            ),
            ["1.md", "2.md", self.pagesFile(arrange=["2.md"])],
        )

        self.assertEqual(
            navigation,
            [
                ("Page 2", "/2"),
                ("Link 1", "https://example.com"),
                ("Page 1", "/1"),
                ("Link 2", "https://example.com"),
            ],
        )

    def test_collapsed(self):
        navigation = self.mkdocs(
            self.createConfig(collapse_single_pages=True),
            [
                ("a", ["1.md", "2.md"]),
                ("b", ["3.md"]),
                self.pagesFile(arrange=["b", "a"]),
            ],
        )

        self.assertEqual(navigation, [("3", "/b/3"), ("A", [("1", "/a/1"), ("2", "/a/2")])])

    def test_duplicates(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                "2.md",
                "3.md",
                self.pagesFile(arrange=["2.md", "2.md", "3.md", "1.md", "3.md"]),
            ],
        )

        self.assertEqual(
            navigation,
            [("2", "/2"), ("2", "/2"), ("3", "/3"), ("1", "/1"), ("3", "/3")],
        )

    def test_duplicate_entry(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"1": "1.md"}, {"2": "2.md"}, {"1": "1.md"}, {"3": "3.md"}]),
            [*self.pages123, self.pagesFile(arrange=["2.md", "1.md", "3.md"])],
        )

        self.assertEqual(navigation, [("2", "/2"), ("1", "/1"), ("3", "/3")])

    def test_duplicate_config_entry(self):
        navigation = self.mkdocs(
            self.config,
            [*self.pages123, self.pagesFile(arrange=["1.md", "2.md", "1.md"])],
        )

        self.assertEqual(navigation, [("1", "/1"), ("2", "/2"), ("1", "/1"), ("3", "/3")])

    def test_entry_not_found(self):
        with self.assertRaises(NavEntryNotFound):
            self.mkdocs(
                self.config,
                [
                    *self.pages123,
                    self.pagesFile(arrange=["2.md", "3.md", "1.md", "d.md"]),
                ],
            )

    def test_entry_not_found_strict(self):
        with self.assertRaises(NavEntryNotFound):
            self.mkdocs(
                self.createConfig(strict=True),
                [
                    *self.pages123,
                    self.pagesFile(arrange=["2.md", "3.md", "1.md", "d.md"]),
                ],
            )

    def test_entry_not_found_not_strict(self):
        with self.assertWarns(NavEntryNotFound):
            self.mkdocs(
                self.createConfig(strict=False),
                [
                    *self.pages123,
                    self.pagesFile(arrange=["2.md", "3.md", "1.md", "d.md"]),
                ],
            )

    def test_auto_index(self):
        navigation = self.mkdocs(self.config, ["before_index.md", "index.md"])

        self.assertEqual(navigation, [("Home", "/"), ("Before index", "/before_index")])
