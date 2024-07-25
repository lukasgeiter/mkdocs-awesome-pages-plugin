import pytest
from mkdocs import __version__ as mkdocs_version

from ...meta import DuplicateRestItemError
from ...navigation import NavEntryNotFound
from .base import E2ETestCase


class TestMkdocsNav(E2ETestCase):
    def test_meta_title(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"A": ["a/2.md", "a/1.md"]}]),
            [("a", ["1.md", "2.md", "3.md", self.pagesFile(title="Title A")])],
        )

        self.assertEqual(navigation, [("A", [("2", "/a/2"), ("1", "/a/1")])])

    def test_meta_nav(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"B": ["a/2.md", "a/1.md"]}]),
            [("a", ["1.md", "2.md", "3.md", self.pagesFile(nav=["3.md", "..."])])],
        )

        self.assertEqual(navigation, [("B", [("2", "/a/2"), ("1", "/a/1")])])

    def test_meta_nav_link(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"B": ["a/2.md", "a/1.md"]}]),
            [
                (
                    "a",
                    [
                        "1.md",
                        "2.md",
                        "3.md",
                        self.pagesFile(nav=["...", {"Link": "https://lukasgeiter.com"}]),
                    ],
                )
            ],
        )

        self.assertEqual(navigation, [("B", [("2", "/a/2"), ("1", "/a/1")])])

    def test_meta_hide(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"B": ["a/2.md", "a/1.md"]}]),
            [("a", ["1.md", "2.md", "3.md", self.pagesFile(hide=True)])],
        )

        self.assertEqual(navigation, [("B", [("2", "/a/2"), ("1", "/a/1")])])

    def test_meta_order(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"B": ["a/1.md", "a/2.md"]}]),
            [("a", ["1.md", "2.md", "3.md", self.pagesFile(order="desc")])],
        )

        self.assertEqual(navigation, [("B", [("1", "/a/1"), ("2", "/a/2")])])

    def test_meta_collapse(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"B": ["a/1.md"]}]),
            [("a", ["1.md", "2.md", self.pagesFile(collapse_single_pages=True)])],
        )

        self.assertEqual(navigation, [("B", [("1", "/a/1")])])

    def test_meta_collapse_nested(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"B": [{"C": ["a/1.md"]}]}]),
            [("a", ["1.md", "2.md", self.pagesFile(collapse_single_pages=True)])],
        )

        self.assertEqual(navigation, [("B", [("C", [("1", "/a/1")])])])

    def test_meta_collapse_global(self):
        navigation = self.mkdocs(
            self.createConfig(collapse_single_pages=True, mkdocs_nav=[{"B": ["a/1.md"]}]),
            [("a", ["1.md", "2.md"])],
        )

        self.assertEqual(navigation, [("B", [("1", "/a/1")])])


class TestMkdocsNavRest(E2ETestCase):
    def test_start(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=["...", "2.md", "1.md"]),
            ["1.md", "2.md", "3.md"],
        )

        self.assertEqual(navigation, [("3", "/3"), ("2", "/2"), ("1", "/1")])

    def test_middle(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=["2.md", "...", "1.md"]),
            ["1.md", "2.md", "3.md"],
        )

        self.assertEqual(navigation, [("2", "/2"), ("3", "/3"), ("1", "/1")])

    def test_end(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=["2.md", "1.md", "..."]),
            ["1.md", "2.md", "3.md"],
        )

        self.assertEqual(navigation, [("2", "/2"), ("1", "/1"), ("3", "/3")])

    @pytest.mark.skipif(
        mkdocs_version >= "1.6.0",
        reason="Handling of duplicates changed with version 1.6",
    )
    def test_duplicate_item_old(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"2a": "2.md"}, {"2b": "2.md"}, "1.md", "..."]),
            ["1.md", "2.md", "3.md"],
        )

        self.assertEqual(navigation, [("2a", "/2"), ("2b", "/2"), ("1", "/1"), ("3", "/3")])

    @pytest.mark.skipif(
        mkdocs_version < "1.6.0",
        reason="Handling of duplicates changed with version 1.6",
    )
    def test_duplicate_item_new(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"2a": "2.md"}, {"2b": "2.md"}, "1.md", "..."]),
            ["1.md", "2.md", "3.md"],
        )

        self.assertEqual(navigation, [("2a", "/2"), ("2a", "/2"), ("1", "/1"), ("3", "/3")])

    def test_duplicate_rest_token(self):
        with self.assertRaises(DuplicateRestItemError):
            self.mkdocs(
                self.createConfig(mkdocs_nav=["...", "1.md", "..."]),
                ["1.md", "2.md", "3.md"],
            )

    def test_titles(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"Title 2": "2.md"}, {"Title 1": "1.md"}, "..."]),
            ["1.md", "2.md", "3.md"],
        )

        self.assertEqual(navigation, [("Title 2", "/2"), ("Title 1", "/1"), ("3", "/3")])

    def test_links(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=["2.md", {"Link": "https://lukasgeiter.com"}, "..."]),
            ["1.md", "2.md", "3.md"],
        )

        self.assertEqual(
            navigation,
            [
                ("2", "/2"),
                ("Link", "https://lukasgeiter.com"),
                ("1", "/1"),
                ("3", "/3"),
            ],
        )

    def test_sections(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=["...", {"C": ["a/2.md", "a/1.md", "b/3.md"]}]),
            [("a", ["1.md", "2.md", "3.md"]), ("b", ["1.md", "2.md", "3.md"])],
        )

        self.assertEqual(
            navigation,
            [
                ("A", [("3", "/a/3")]),
                ("B", [("1", "/b/1"), ("2", "/b/2")]),
                ("C", [("2", "/a/2"), ("1", "/a/1"), ("3", "/b/3")]),
            ],
        )

    def test_sections_nested_rest(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"C": ["a/2.md", "a/1.md", "b/3.md"]}, {"Rest": ["..."]}]),
            [("a", ["1.md", "2.md", "3.md"]), ("b", ["1.md", "2.md", "3.md"])],
            dummy_pages=False,
        )

        self.assertEqual(
            navigation,
            [
                ("C", [("2", "/a/2"), ("1", "/a/1"), ("3", "/b/3")]),
                (
                    "Rest",
                    [("A", [("3", "/a/3")]), ("B", [("1", "/b/1"), ("2", "/b/2")])],
                ),
            ],
        )

    @pytest.mark.skipif(
        mkdocs_version >= "1.3.0",
        reason="Since version 1.3 MkDocs validates nav and Dict type is invalid.",
    )
    def test_sections_nested_rest_dict(self):
        navigation = self.mkdocs(
            self.createConfig(
                mkdocs_nav=[
                    {"C": ["a/2.md", "a/1.md", "b/3.md"]},
                    {"Rest": {"Dict": ["..."]}},
                ]
            ),
            [("a", ["1.md", "2.md", "3.md"]), ("b", ["1.md", "2.md", "3.md"])],
            dummy_pages=False,
        )

        self.assertEqual(
            navigation,
            [
                ("C", [("2", "/a/2"), ("1", "/a/1"), ("3", "/b/3")]),
                (
                    "Rest",
                    [
                        (
                            "Dict",
                            [
                                ("A", [("3", "/a/3")]),
                                ("B", [("1", "/b/1"), ("2", "/b/2")]),
                            ],
                        )
                    ],
                ),
            ],
        )

    def test_meta_title(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"C": ["a/2.md", "a/1.md"]}, "..."]),
            [
                ("a", ["1.md", "2.md", "3.md", self.pagesFile(title="Title A")]),
                ("b", ["1.md", "2.md", self.pagesFile(title="Title B")]),
            ],
        )

        self.assertEqual(
            navigation,
            [
                ("C", [("2", "/a/2"), ("1", "/a/1")]),
                ("Title A", [("3", "/a/3")]),
                ("Title B", [("1", "/b/1"), ("2", "/b/2")]),
            ],
        )

    def test_meta_nav(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"B": ["a/2.md", "a/1.md"]}, "..."]),
            [
                (
                    "a",
                    [
                        "1.md",
                        "2.md",
                        "3.md",
                        "4.md",
                        self.pagesFile(nav=["4.md", "..."]),
                    ],
                )
            ],
        )

        self.assertEqual(
            navigation,
            [
                ("B", [("2", "/a/2"), ("1", "/a/1")]),
                ("A", [("4", "/a/4"), ("3", "/a/3")]),
            ],
        )

    def test_meta_nav_conflict(self):
        with self.assertRaises(NavEntryNotFound):
            self.mkdocs(
                self.createConfig(mkdocs_nav=["a/2.md", "..."]),
                [("a", ["1.md", "2.md", "3.md", self.pagesFile(nav=["2.md", "..."])])],
            )

    def test_meta_nav_link(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"B": ["a/2.md", "a/1.md"]}, "..."]),
            [
                (
                    "a",
                    [
                        "1.md",
                        "2.md",
                        "3.md",
                        "4.md",
                        self.pagesFile(nav=["...", {"Link": "https://lukasgeiter.com"}]),
                    ],
                )
            ],
        )

        self.assertEqual(
            navigation,
            [
                ("B", [("2", "/a/2"), ("1", "/a/1")]),
                (
                    "A",
                    [("3", "/a/3"), ("4", "/a/4"), ("Link", "https://lukasgeiter.com")],
                ),
            ],
        )

    def test_meta_hide(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"B": ["a/2.md", "a/1.md"]}, "..."]),
            [("a", ["1.md", "2.md", "3.md", self.pagesFile(hide=True)])],
        )

        self.assertEqual(navigation, [("B", [("2", "/a/2"), ("1", "/a/1")])])

    def test_meta_order(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"B": ["a/1.md", "a/2.md"]}, "..."]),
            [("a", ["1.md", "2.md", "3.md", "4.md", self.pagesFile(order="desc")])],
        )

        self.assertEqual(
            navigation,
            [
                ("B", [("1", "/a/1"), ("2", "/a/2")]),
                (
                    "A",
                    [
                        ("4", "/a/4"),
                        ("3", "/a/3"),
                    ],
                ),
            ],
        )

    def test_meta_collapse(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"B": ["a/1.md"]}, "..."]),
            [("a", ["1.md", "2.md", self.pagesFile(collapse_single_pages=True)])],
        )

        self.assertEqual(navigation, [("B", [("1", "/a/1")]), ("2", "/a/2")])

    def test_meta_collapse_nested(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"B": [{"C": ["a/1.md"]}]}, {"Rest": ["..."]}]),
            [("a", ["1.md", "2.md", self.pagesFile(collapse_single_pages=True)])],
            dummy_pages=False,
        )

        self.assertEqual(navigation, [("B", [("C", [("1", "/a/1")])]), ("Rest", [("2", "/a/2")])])

    def test_meta_collapse_global(self):
        navigation = self.mkdocs(
            self.createConfig(collapse_single_pages=True, mkdocs_nav=[{"B": ["a/1.md"]}, "..."]),
            [("a", ["1.md", "2.md"])],
        )

        self.assertEqual(navigation, [("B", [("1", "/a/1")]), ("2", "/a/2")])

    def test_flat(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=["... | flat", {"C": ["a/2.md", "a/1.md", "b/3.md"]}]),
            [("a", ["1.md", "2.md", "3.md"]), ("b", ["1.md", "2.md", "3.md"])],
        )

        self.assertEqual(
            navigation,
            [
                ("3", "/a/3"),
                ("1", "/b/1"),
                ("2", "/b/2"),
                ("C", [("2", "/a/2"), ("1", "/a/1"), ("3", "/b/3")]),
            ],
        )


class TestMkdocsNavRestGlob(E2ETestCase):
    def test_pattern_only(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=["2a.md", "... | *a.md"]),
            ["1a.md", "1b.md", "2a.md", "3a.md"],
        )

        self.assertEqual(navigation, [("2a", "/2a"), ("1a", "/1a"), ("3a", "/3a")])

    def test_pattern_and_rest(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=["... | *a.md", "2a.md", "..."]),
            ["1a.md", "1b.md", "2a.md", "3a.md"],
        )

        self.assertEqual(navigation, [("1a", "/1a"), ("3a", "/3a"), ("2a", "/2a"), ("1b", "/1b")])

    def test_multiple_patterns(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=["1c.md", "... | *a.md", "2c.md", "... | *b.md"]),
            ["1a.md", "1b.md", "1c.md", "2a.md", "2b.md", "2c.md"],
        )

        self.assertEqual(
            navigation,
            [
                ("1c", "/1c"),
                ("1a", "/1a"),
                ("2a", "/2a"),
                ("2c", "/2c"),
                ("1b", "/1b"),
                ("2b", "/2b"),
            ],
        )

    def test_overlapping_patterns(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=["... | *a.md", "1c.md", "... | 2*.md"]),
            ["1a.md", "1b.md", "1c.md", "2a.md", "2b.md", "2c.md"],
        )

        self.assertEqual(
            navigation,
            [("1a", "/1a"), ("2a", "/2a"), ("1c", "/1c"), ("2b", "/2b"), ("2c", "/2c")],
        )

    def test_folder(self):
        navigation = self.mkdocs(
            self.createConfig(
                mkdocs_nav=[
                    "b/1.md",
                    "... | *.md",  # doesn't match anything
                    "b/2.md",
                    "... | a",  # doesn't match anything
                    "b/3.md",
                    "... | a/*.md",
                ]
            ),
            [("a", ["1.md", "2.md", "3.md"]), ("b", ["1.md", "2.md", "3.md"])],
        )

        self.assertEqual(
            navigation,
            [
                ("1", "/b/1"),
                ("2", "/b/2"),
                ("3", "/b/3"),
                ("A", [("1", "/a/1"), ("2", "/a/2"), ("3", "/a/3")]),
            ],
        )

    def test_nested(self):
        navigation = self.mkdocs(
            self.createConfig(
                mkdocs_nav=[
                    "... | **/1.md",
                    {"2": ["... | a/**/2.md"]},
                    {"Rest": ["..."]},
                ]
            ),
            [
                ("a", ["1.md", "2.md", "3.md", ("aa", ["1.md", "2.md"])]),
                ("b", ["1.md", "2.md", "3.md"]),
            ],
            dummy_pages=False,
        )

        self.assertEqual(
            navigation,
            [
                ("A", [("1", "/a/1"), ("Aa", [("1", "/a/aa/1")])]),
                ("B", [("1", "/b/1")]),
                ("2", [("A", [("2", "/a/2"), ("Aa", [("2", "/a/aa/2")])])]),
                (
                    "Rest",
                    [("A", [("3", "/a/3")]), ("B", [("2", "/b/2"), ("3", "/b/3")])],
                ),
            ],
        )

    def test_precedence(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=["...", {"1": ["... | 1*.md"]}, "... | *[ab].md"]),
            ["1.md", "1a.md", "1b.md", "2.md", "2a.md", "2b.md"],
            dummy_pages=False,
        )

        self.assertEqual(
            navigation,
            [
                ("2", "/2"),
                ("1", [("1", "/1"), ("1a", "/1a"), ("1b", "/1b")]),
                ("2a", "/2a"),
                ("2b", "/2b"),
            ],
        )

    def test_duplicate_pattern(self):
        with self.assertRaises(DuplicateRestItemError):
            self.mkdocs(
                self.createConfig(mkdocs_nav=["... | a*.md", "1.md", "... | a*.md"]),
                ["1.md", "2.md", "3.md"],
            )

    def test_flat(self):
        navigation = self.mkdocs(
            self.createConfig(
                mkdocs_nav=[
                    "... | flat | **/1.md",
                    {"2": ["... | flat | a/**/2.md"]},
                    {"Rest": ["... | flat"]},
                ]
            ),
            [
                ("a", ["1.md", "2.md", "3.md", ("aa", ["1.md", "2.md"])]),
                ("b", ["1.md", "2.md", "3.md"]),
            ],
            dummy_pages=False,
        )

        self.assertEqual(
            navigation,
            [
                ("1", "/a/1"),
                ("1", "/a/aa/1"),
                ("1", "/b/1"),
                ("2", [("2", "/a/2"), ("2", "/a/aa/2")]),
                ("Rest", [("3", "/a/3"), ("2", "/b/2"), ("3", "/b/3")]),
            ],
        )


class TestMkdocsNavRestRegex(E2ETestCase):
    def test_pattern_only(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=["2a.md", r"... | regex=.+a\.md"]),
            ["1a.md", "1b.md", "2a.md", "3a.md"],
        )

        self.assertEqual(navigation, [("2a", "/2a"), ("1a", "/1a"), ("3a", "/3a")])

    def test_pattern_and_rest(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[r"... | regex=.+a\.md", "2a.md", "..."]),
            ["1a.md", "1b.md", "2a.md", "3a.md"],
        )

        self.assertEqual(navigation, [("1a", "/1a"), ("3a", "/3a"), ("2a", "/2a"), ("1b", "/1b")])

    def test_multiple_patterns(self):
        navigation = self.mkdocs(
            self.createConfig(
                mkdocs_nav=[
                    "1c.md",
                    r"... | regex=.+a\.md",
                    "2c.md",
                    r"... | regex=.+b\.md",
                ]
            ),
            ["1a.md", "1b.md", "1c.md", "2a.md", "2b.md", "2c.md"],
        )

        self.assertEqual(
            navigation,
            [
                ("1c", "/1c"),
                ("1a", "/1a"),
                ("2a", "/2a"),
                ("2c", "/2c"),
                ("1b", "/1b"),
                ("2b", "/2b"),
            ],
        )

    def test_overlapping_patterns(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[r"... | regex=.+a\.md", "1c.md", r"... | regex=2.+\.md"]),
            ["1a.md", "1b.md", "1c.md", "2a.md", "2b.md", "2c.md"],
        )

        self.assertEqual(
            navigation,
            [("1a", "/1a"), ("2a", "/2a"), ("1c", "/1c"), ("2b", "/2b"), ("2c", "/2c")],
        )

    def test_folder(self):
        navigation = self.mkdocs(
            self.createConfig(
                mkdocs_nav=[
                    "b/1.md",
                    r"... | regex=^\w+\.md$",  # doesn't match anything
                    "b/2.md",
                    r"... | regex=^\w+$",  # doesn't match anything
                    "b/3.md",
                    r"... | regex=^a/\w+\.md$",
                ]
            ),
            [("a", ["1.md", "2.md", "3.md"]), ("b", ["1.md", "2.md", "3.md"])],
        )

        self.assertEqual(
            navigation,
            [
                ("1", "/b/1"),
                ("2", "/b/2"),
                ("3", "/b/3"),
                ("A", [("1", "/a/1"), ("2", "/a/2"), ("3", "/a/3")]),
            ],
        )

    def test_nested(self):
        navigation = self.mkdocs(
            self.createConfig(
                mkdocs_nav=[
                    r"... | regex=^.*/1\.md$",
                    {"2": [r"... | regex=^a/(.*/|)2\.md$"]},
                    {"Rest": ["..."]},
                ]
            ),
            [
                ("a", ["1.md", "2.md", "3.md", ("aa", ["1.md", "2.md"])]),
                ("b", ["1.md", "2.md", "3.md"]),
            ],
            dummy_pages=False,
        )

        self.assertEqual(
            navigation,
            [
                ("A", [("1", "/a/1"), ("Aa", [("1", "/a/aa/1")])]),
                ("B", [("1", "/b/1")]),
                ("2", [("A", [("2", "/a/2"), ("Aa", [("2", "/a/aa/2")])])]),
                (
                    "Rest",
                    [("A", [("3", "/a/3")]), ("B", [("2", "/b/2"), ("3", "/b/3")])],
                ),
            ],
        )

    def test_precedence(self):
        navigation = self.mkdocs(
            self.createConfig(
                mkdocs_nav=[
                    "...",
                    {"1": [r"... | regex=1\w*\.md"]},
                    r"... | regex=\w*[ab]\.md",
                ]
            ),
            ["1.md", "1a.md", "1b.md", "2.md", "2a.md", "2b.md"],
            dummy_pages=False,
        )

        self.assertEqual(
            navigation,
            [
                ("2", "/2"),
                ("1", [("1", "/1"), ("1a", "/1a"), ("1b", "/1b")]),
                ("2a", "/2a"),
                ("2b", "/2b"),
            ],
        )

    def test_duplicate_pattern(self):
        with self.assertRaises(DuplicateRestItemError):
            self.mkdocs(
                self.createConfig(mkdocs_nav=[r"... | regex=a.+\.md", "1.md", r"... | regex=a.+\.md"]),
                ["1.md", "2.md", "3.md"],
            )

    def test_flat(self):
        navigation = self.mkdocs(
            self.createConfig(
                mkdocs_nav=[
                    r"... | flat | regex=^.*/1\.md$",
                    {"2": [r"... | flat | regex=^a/(.*/|)2\.md$"]},
                    {"Rest": ["... | flat"]},
                ]
            ),
            [
                ("a", ["1.md", "2.md", "3.md", ("aa", ["1.md", "2.md"])]),
                ("b", ["1.md", "2.md", "3.md"]),
            ],
            dummy_pages=False,
        )

        self.assertEqual(
            navigation,
            [
                ("1", "/a/1"),
                ("1", "/a/aa/1"),
                ("1", "/b/1"),
                ("2", [("2", "/a/2"), ("2", "/a/aa/2")]),
                ("Rest", [("3", "/a/3"), ("2", "/b/2"), ("3", "/b/3")]),
            ],
        )
