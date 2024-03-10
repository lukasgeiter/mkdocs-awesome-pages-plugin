from ...meta import Meta, MetaNavItem, MetaNavRestItem
from ...navigation import NavEntryNotFound
from .base import NavigationTestCase


class TestNav(NavigationTestCase):
    def test_all_listed(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("2"),
                self.page("3"),
                Meta(nav=[MetaNavItem("2.md"), MetaNavItem("3.md"), MetaNavItem("1.md")]),
            ]
        )

        self.assertNavigationEqual(navigation.items, [self.page("2"), self.page("3"), self.page("1")])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_some_listed(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("2"),
                self.page("3"),
                Meta(nav=[MetaNavItem("3.md"), MetaNavItem("1.md")]),
            ]
        )

        self.assertNavigationEqual(navigation.items, [self.page("3"), self.page("1")])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_none_listed(self):
        navigation = self.createAwesomeNavigation([self.page("1"), self.page("2"), self.page("3"), Meta(nav=[])])

        self.assertNavigationEqual(navigation.items, [])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_rest(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("2"),
                self.page("3"),
                self.page("4"),
                Meta(
                    nav=[
                        MetaNavItem("3.md"),
                        MetaNavRestItem("..."),
                        MetaNavItem("1.md"),
                    ]
                ),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [self.page("3"), self.page("2"), self.page("4"), self.page("1")],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_rest_empty(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("2"),
                Meta(
                    nav=[
                        MetaNavItem("2.md"),
                        MetaNavRestItem("..."),
                        MetaNavItem("1.md"),
                    ]
                ),
            ]
        )

        self.assertNavigationEqual(navigation.items, [self.page("2"), self.page("1")])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_rest_glob(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("2a"),
                self.page("2b"),
                self.page("3"),
                Meta(
                    nav=[
                        MetaNavItem("1.md"),
                        MetaNavRestItem("... | 2*.md"),
                        MetaNavItem("1.md"),
                    ]
                ),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [self.page("1"), self.page("2a"), self.page("2b"), self.page("1")],
        )

    def test_rest_glob_section(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("a"),
                self.page("b"),
                self.section(
                    "Section A",
                    [
                        self.page("1a", "a/1a.md"),
                        self.page("1b", "a/1b.md"),
                        self.page("2a", "a/2a.md"),
                        self.page("2b", "a/2b.md"),
                        Meta(
                            nav=[
                                MetaNavRestItem("... | *b.md"),
                                MetaNavRestItem("..."),
                            ],
                            path="a/.pages",
                        ),
                    ],
                    "a",
                ),
                Meta(nav=[MetaNavRestItem("... | a*"), MetaNavItem("b.md")]),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [
                self.page("a"),
                self.section(
                    "Section A",
                    [
                        self.page("1b", "a/1b.md"),
                        self.page("2b", "a/2b.md"),
                        self.page("1a", "a/1a.md"),
                        self.page("2a", "a/2a.md"),
                    ],
                    "a",
                ),
                self.page("b"),
            ],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_rest_glob_precedence(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("1a"),
                self.page("1b"),
                self.page("2"),
                self.page("2a"),
                self.page("2b"),
                Meta(
                    nav=[
                        MetaNavRestItem("..."),
                        MetaNavItem("/", "Link 1"),
                        MetaNavRestItem("... | 1*.md"),
                        MetaNavItem("/", "Link 2"),
                        MetaNavRestItem("... | *[ab].md"),
                    ]
                ),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [
                self.page("2"),
                self.link("Link 1", "/"),
                self.page("1"),
                self.page("1a"),
                self.page("1b"),
                self.link("Link 2", "/"),
                self.page("2a"),
                self.page("2b"),
            ],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_rest_regex(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("2a"),
                self.page("2b"),
                self.page("3"),
                Meta(
                    nav=[
                        MetaNavItem("1.md"),
                        MetaNavRestItem(r"... | regex=2\w*\.md"),
                        MetaNavItem("1.md"),
                    ]
                ),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [self.page("1"), self.page("2a"), self.page("2b"), self.page("1")],
        )

    def test_rest_regex_section(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("a"),
                self.page("b"),
                self.section(
                    "Section A",
                    [
                        self.page("1a", "a/1a.md"),
                        self.page("1b", "a/1b.md"),
                        self.page("2a", "a/2a.md"),
                        self.page("2b", "a/2b.md"),
                        Meta(
                            nav=[
                                MetaNavRestItem(r"... | regex=\w*b\.md"),
                                MetaNavRestItem("..."),
                            ],
                            path="a/.pages",
                        ),
                    ],
                    "a",
                ),
                Meta(nav=[MetaNavRestItem(r"... | regex=a\w*"), MetaNavItem("b.md")]),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [
                self.page("a"),
                self.section(
                    "Section A",
                    [
                        self.page("1b", "a/1b.md"),
                        self.page("2b", "a/2b.md"),
                        self.page("1a", "a/1a.md"),
                        self.page("2a", "a/2a.md"),
                    ],
                    "a",
                ),
                self.page("b"),
            ],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_rest_regex_precedence(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("1a"),
                self.page("1b"),
                self.page("2"),
                self.page("2a"),
                self.page("2b"),
                Meta(
                    nav=[
                        MetaNavRestItem("..."),
                        MetaNavItem("/", "Link 1"),
                        MetaNavRestItem(r"... | regex=1\w*\.md"),
                        MetaNavItem("/", "Link 2"),
                        MetaNavRestItem(r"... | regex=\w*[ab]\.md"),
                    ]
                ),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [
                self.page("2"),
                self.link("Link 1", "/"),
                self.page("1"),
                self.page("1a"),
                self.page("1b"),
                self.link("Link 2", "/"),
                self.page("2a"),
                self.page("2b"),
            ],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_title(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("2"),
                Meta(nav=[MetaNavItem("2.md", "Title"), MetaNavItem("1.md")]),
            ]
        )

        self.assertNavigationEqual(navigation.items, [self.page("Title", "2.md"), self.page("1")])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_existing_link(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("2"),
                self.link("Link"),
                Meta(nav=[MetaNavItem("2.md"), MetaNavItem("1.md")]),
            ]
        )

        self.assertNavigationEqual(navigation.items, [self.page("2"), self.page("1")])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_existing_link_rest(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("2"),
                self.link("Link"),
                Meta(
                    nav=[
                        MetaNavItem("2.md"),
                        MetaNavRestItem("..."),
                        MetaNavItem("1.md"),
                    ]
                ),
            ]
        )

        self.assertNavigationEqual(navigation.items, [self.page("2"), self.link("Link"), self.page("1")])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_added_link(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("2"),
                Meta(
                    nav=[
                        MetaNavItem("2.md"),
                        MetaNavItem("Url", "Link"),
                        MetaNavItem("1.md"),
                    ]
                ),
            ]
        )

        self.assertNavigationEqual(navigation.items, [self.page("2"), self.link("Link", "Url"), self.page("1")])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_duplicate_list_item(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("2"),
                Meta(nav=[MetaNavItem("2.md"), MetaNavItem("1.md"), MetaNavItem("2.md")]),
            ]
        )

        self.assertNavigationEqual(navigation.items, [self.page("2"), self.page("1"), self.page("2")])

    def test_duplicate_navigation_item(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("2a", "2.md"),
                self.page("2b", "2.md"),
                Meta(nav=[MetaNavItem("2.md"), MetaNavItem("1.md")]),
            ]
        )

        self.assertNavigationEqual(navigation.items, [self.page("2b", "2.md"), self.page("1")])

    def test_not_found(self):
        with self.assertRaises(NavEntryNotFound):
            self.createAwesomeNavigation(
                [
                    self.page("1"),
                    self.page("2"),
                    Meta(nav=[MetaNavItem("1.md"), MetaNavItem("3.md")]),
                ]
            )

    def test_not_found_not_strict(self):
        with self.assertWarns(NavEntryNotFound):
            self.createAwesomeNavigation(
                [
                    self.page("1"),
                    self.page("2"),
                    Meta(nav=[MetaNavItem("1.md"), MetaNavItem("3.md")]),
                ],
                strict=False,
            )

    def test_virtual_section(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("2a"),
                self.page("2b"),
                self.page("2c"),
                self.page("3a"),
                self.page("3b"),
                self.page("3c"),
                self.page("4"),
                Meta(
                    nav=[
                        MetaNavItem("4.md"),
                        MetaNavItem([MetaNavItem("2a.md"), MetaNavItem("3a.md")], "AA"),
                        MetaNavRestItem("..."),
                        MetaNavItem([MetaNavItem("2b.md"), MetaNavItem("3b.md")], "BB"),
                        MetaNavItem("1.md"),
                    ]
                ),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [
                self.page("4"),
                self.section("AA", [self.page("2a"), self.page("3a")]),
                self.page("2c"),
                self.page("3c"),
                self.section("BB", [self.page("2b"), self.page("3b")]),
                self.page("1"),
            ],
        )
        self.assertValidNavigation(navigation.to_mkdocs())
