import pytest
from mkdocs import __version__ as mkdocs_version

from ...meta import DuplicateRestItemError
from ...navigation import NavEntryNotFound
from .base import E2ETestCase


class TestNav(E2ETestCase):
    def test_all_listed(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                "2.md",
                ("a", ["1.md", "2.md", self.pagesFile(nav=["2.md", "1.md"])]),
                self.pagesFile(nav=["a", "2.md", "1.md"]),
            ],
        )

        self.assertEqual(
            navigation,
            [("A", [("2", "/a/2"), ("1", "/a/1")]), ("2", "/2"), ("1", "/1")],
        )

    def test_some_listed(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                "2.md",
                ("a", ["1.md", "2.md", self.pagesFile(nav=["1.md"])]),
                self.pagesFile(nav=["a", "1.md"]),
            ],
        )

        self.assertEqual(navigation, [("A", [("1", "/a/1")]), ("1", "/1")])

    def test_none_listed(self):
        navigation = self.mkdocs(self.config, ["1.md", ("a", ["1.md", "2.md", self.pagesFile(nav=[])])])

        self.assertEqual(navigation, [("1", "/1")])

    def test_rest(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                "2.md",
                (
                    "a",
                    [
                        "1.md",
                        "2.md",
                        "3.md",
                        "4.md",
                        self.pagesFile(nav=["2.md", "...", "1.md"]),
                    ],
                ),
                self.pagesFile(nav=["2.md", "..."]),
            ],
        )

        self.assertEqual(
            navigation,
            [
                ("2", "/2"),
                ("1", "/1"),
                ("A", [("2", "/a/2"), ("3", "/a/3"), ("4", "/a/4"), ("1", "/a/1")]),
            ],
        )

    def test_rest_empty(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                ("a", ["1.md", "2.md", self.pagesFile(nav=["2.md", "...", "1.md"])]),
                self.pagesFile(nav=["a", "...", "1.md"]),
            ],
        )

        self.assertEqual(navigation, [("A", [("2", "/a/2"), ("1", "/a/1")]), ("1", "/1")])

    def test_rest_glob(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                "2a.md",
                "2b.md",
                "3.md",
                self.pagesFile(nav=["1.md", "... | 2*.md", "1.md"]),
            ],
        )

        self.assertEqual(navigation, [("1", "/1"), ("2a", "/2a"), ("2b", "/2b"), ("1", "/1")])

    def test_rest_glob_section(self):
        navigation = self.mkdocs(
            self.config,
            [
                "a.md",
                "b.md",
                (
                    "a",
                    [
                        "1a.md",
                        "1b.md",
                        "2a.md",
                        "2b.md",
                        self.pagesFile(nav=["... | *b.md", "..."]),
                    ],
                ),
                self.pagesFile(nav=["... | a*", "b.md"]),
            ],
        )

        self.assertEqual(
            navigation,
            [
                ("A", "/a"),
                (
                    "A",
                    [
                        ("1b", "/a/1b"),
                        ("2b", "/a/2b"),
                        ("1a", "/a/1a"),
                        ("2a", "/a/2a"),
                    ],
                ),
                ("B", "/b"),
            ],
        )

    def test_rest_glob_precedence(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                "1a.md",
                "1b.md",
                "2.md",
                "2a.md",
                "2b.md",
                self.pagesFile(
                    nav=[
                        "...",
                        {"Link 1": "/link1"},
                        "... | 1*.md",
                        {"Link 2": "/link2"},
                        "... | *[ab].md",
                    ]
                ),
            ],
        )

        self.assertEqual(
            navigation,
            [
                ("2", "/2"),
                ("Link 1", "/link1"),
                ("1", "/1"),
                ("1a", "/1a"),
                ("1b", "/1b"),
                ("Link 2", "/link2"),
                ("2a", "/2a"),
                ("2b", "/2b"),
            ],
        )

    def test_rest_regex(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                "2a.md",
                "2b.md",
                "3.md",
                self.pagesFile(nav=["1.md", r"... | regex=2\w*\.md", "1.md"]),
            ],
        )

        self.assertEqual(navigation, [("1", "/1"), ("2a", "/2a"), ("2b", "/2b"), ("1", "/1")])

    def test_rest_regex_section(self):
        navigation = self.mkdocs(
            self.config,
            [
                "a.md",
                "b.md",
                (
                    "a",
                    [
                        "1a.md",
                        "1b.md",
                        "2a.md",
                        "2b.md",
                        self.pagesFile(nav=[r"... | regex=\w*b\.md", "..."]),
                    ],
                ),
                self.pagesFile(nav=[r"... | regex=a\w*", "b.md"]),
            ],
        )

        self.assertEqual(
            navigation,
            [
                ("A", "/a"),
                (
                    "A",
                    [
                        ("1b", "/a/1b"),
                        ("2b", "/a/2b"),
                        ("1a", "/a/1a"),
                        ("2a", "/a/2a"),
                    ],
                ),
                ("B", "/b"),
            ],
        )

    def test_rest_regex_precedence(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                "1a.md",
                "1b.md",
                "2.md",
                "2a.md",
                "2b.md",
                self.pagesFile(
                    nav=[
                        "...",
                        {"Link 1": "/link1"},
                        r"... | regex=1\w*\.md",
                        {"Link 2": "/link2"},
                        r"... | regex=\w*[ab]\.md",
                    ]
                ),
            ],
        )

        self.assertEqual(
            navigation,
            [
                ("2", "/2"),
                ("Link 1", "/link1"),
                ("1", "/1"),
                ("1a", "/1a"),
                ("1b", "/1b"),
                ("Link 2", "/link2"),
                ("2a", "/2a"),
                ("2b", "/2b"),
            ],
        )

    def test_title(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                "2.md",
                (
                    "a",
                    ["1.md", "2.md", self.pagesFile(nav=["1.md", {"Title 2": "2.md"}])],
                ),
                self.pagesFile(nav=[{"Title 1": "1.md"}, "2.md", {"Title A": "a"}]),
            ],
        )

        self.assertEqual(
            navigation,
            [
                ("Title 1", "/1"),
                ("2", "/2"),
                ("Title A", [("1", "/a/1"), ("Title 2", "/a/2")]),
            ],
        )

    def test_title_conflict(self):
        navigation = self.mkdocs(
            self.config,
            [
                ("a", ["1.md", "2.md", self.pagesFile(title="Title Meta")]),
                self.pagesFile(nav=[{"Title Nav": "a"}, "..."]),
            ],
        )

        self.assertEqual(navigation, [("Title Meta", [("1", "/a/1"), ("2", "/a/2")])])

    def test_link(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                (
                    "a",
                    [
                        "1.md",
                        self.pagesFile(
                            nav=[
                                "...",
                                {"Internal Link": "/link"},
                                {"External Link": "https://lukasgeiter.com"},
                            ]
                        ),
                    ],
                ),
                self.pagesFile(
                    nav=[
                        "...",
                        {"Internal Link": "/link"},
                        {"External Link": "https://lukasgeiter.com"},
                    ]
                ),
            ],
        )

        self.assertEqual(
            navigation,
            [
                ("1", "/1"),
                (
                    "A",
                    [
                        ("1", "/a/1"),
                        ("Internal Link", "/link"),
                        ("External Link", "https://lukasgeiter.com"),
                    ],
                ),
                ("Internal Link", "/link"),
                ("External Link", "https://lukasgeiter.com"),
            ],
        )

    def test_collapsed(self):
        navigation = self.mkdocs(
            self.createConfig(collapse_single_pages=True),
            [
                ("a", ["1.md", "2.md"]),
                ("b", ["1.md"]),
                self.pagesFile(arrange=["b", "a"]),
            ],
        )

        self.assertEqual(navigation, [("1", "/b/1"), ("A", [("1", "/a/1"), ("2", "/a/2")])])

    @pytest.mark.skipif(
        mkdocs_version >= "1.6.0",
        reason="Handling of duplicates changed with version 1.6",
    )
    def test_duplicate_file_old(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"1a": "1.md"}, {"2": "2.md"}, {"1b": "1.md"}]),
            ["1.md", "2.md", self.pagesFile(nav=["2.md", "1.md"])],
        )

        self.assertEqual(navigation, [("2", "/2"), ("1b", "/1")])

    @pytest.mark.skipif(
        mkdocs_version < "1.6.0",
        reason="Handling of duplicates changed with version 1.6",
    )
    def test_duplicate_file_new(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"1a": "1.md"}, {"2": "2.md"}, {"1b": "1.md"}]),
            ["1.md", "2.md", self.pagesFile(nav=["2.md", "1.md"])],
        )

        self.assertEqual(navigation, [("2", "/2"), ("1a", "/1")])

    @pytest.mark.skipif(
        mkdocs_version >= "1.6.0",
        reason="Handling of duplicates changed with version 1.6",
    )
    def test_duplicate_file_rest_old(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"1a": "1.md"}, {"2": "2.md"}, {"1b": "1.md"}]),
            ["1.md", "2.md", self.pagesFile(nav=["2.md", "..."])],
        )

        self.assertEqual(navigation, [("2", "/2"), ("1a", "/1"), ("1b", "/1")])

    @pytest.mark.skipif(
        mkdocs_version < "1.6.0",
        reason="Handling of duplicates changed with version 1.6",
    )
    def test_duplicate_file_rest_new(self):
        navigation = self.mkdocs(
            self.createConfig(mkdocs_nav=[{"1a": "1.md"}, {"2": "2.md"}, {"1b": "1.md"}]),
            ["1.md", "2.md", self.pagesFile(nav=["2.md", "..."])],
        )

        self.assertEqual(navigation, [("2", "/2"), ("1a", "/1"), ("1a", "/1")])

    def test_duplicate_entry(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                ("a", ["1.md", "2.md", self.pagesFile(nav=["2.md", "...", "2.md"])]),
                self.pagesFile(nav=["a", "...", "a"]),
            ],
        )

        self.assertEqual(
            navigation,
            [
                ("A", [("2", "/a/2"), ("1", "/a/1"), ("2", "/a/2")]),
                ("1", "/1"),
                ("A", [("2", "/a/2"), ("1", "/a/1"), ("2", "/a/2")]),
            ],
        )

    def test_duplicate_entry_title(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                (
                    "a",
                    [
                        "1.md",
                        "2.md",
                        self.pagesFile(nav=[{"2a": "2.md"}, "...", {"2b": "2.md"}]),
                    ],
                ),
                self.pagesFile(nav=[{"AA": "a"}, "...", {"AB": "a"}]),
            ],
        )

        self.assertEqual(
            navigation,
            [
                ("AB", [("2b", "/a/2"), ("1", "/a/1"), ("2b", "/a/2")]),
                ("1", "/1"),
                ("AB", [("2b", "/a/2"), ("1", "/a/1"), ("2b", "/a/2")]),
            ],
        )

    def test_duplicate_rest_token(self):
        with self.assertRaises(DuplicateRestItemError):
            self.mkdocs(
                self.config,
                ["1.md", "2.md", self.pagesFile(nav=["...", "1.md", "..."])],
            )

    def test_not_found(self):
        with self.assertRaises(NavEntryNotFound):
            self.mkdocs(self.config, [self.pagesFile(nav=["1.md", "..."])])

    def test_not_found_strict(self):
        with self.assertRaises(NavEntryNotFound):
            self.mkdocs(self.createConfig(strict=True), [self.pagesFile(nav=["1.md", "..."])])

    def test_not_found_not_strict(self):
        with self.assertWarns(NavEntryNotFound):
            self.mkdocs(self.createConfig(strict=False), [self.pagesFile(nav=["1.md", "..."])])

    def test_virtual_section(self):
        navigation = self.mkdocs(
            self.config,
            [
                "a.md",
                "b.md",
                (
                    "x",
                    [
                        "1a.md",
                        "1b.md",
                        "2a.md",
                        "2b.md",
                        "3.md",
                        "4.md",
                        self.pagesFile(
                            nav=[
                                "4.md",
                                {"BB": ["... | *b.md"]},
                                "...",
                                {"AA": ["... | *a.md"]},
                            ]
                        ),
                    ],
                ),
                self.pagesFile(nav=["...", "b.md"]),
            ],
        )

        self.assertEqual(
            navigation,
            [
                ("A", "/a"),
                (
                    "X",
                    [
                        ("4", "/x/4"),
                        ("BB", [("1b", "/x/1b"), ("2b", "/x/2b")]),
                        ("3", "/x/3"),
                        ("AA", [("1a", "/x/1a"), ("2a", "/x/2a")]),
                    ],
                ),
                ("B", "/b"),
            ],
        )

    def test_virtual_section_child_pagesfile(self):
        navigation = self.mkdocs(
            self.config,
            [
                "a.md",
                "b.md",
                (
                    "x",
                    [
                        "1.md",
                        "2.md",
                        self.pagesFile(title="X Title", nav=["2.md", "1.md"]),
                    ],
                ),
                self.pagesFile(nav=[{"Virtual Section": ["b.md", "..."]}, "a.md"]),
            ],
            dummy_pages=False,
        )

        self.assertEqual(
            navigation,
            [
                ("Virtual Section", [("B", "/b"), ("X Title", [("2", "/x/2"), ("1", "/x/1")])]),
                ("A", "/a"),
            ],
        )
