from ...meta import Meta
from .base import NavigationTestCase


class TestCollapseGlobalDisabled(NavigationTestCase):
    def test_no_collapse(self):
        navigation = self.createAwesomeNavigation([self.section("Section", [self.page("Page", "section/page.md")])])

        self.assertNavigationEqual(
            navigation.items,
            [self.section("Section", [self.page("Page", "section/page.md")])],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_local(self):
        navigation = self.createAwesomeNavigation(
            [
                self.section(
                    "A",
                    [
                        self.section(
                            "B",
                            [
                                self.section("C", [self.page("Page", "a/b/c/page.md")]),
                                Meta(path="a/b/.pages", collapse=True),
                            ],
                        )
                    ],
                )
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [self.section("A", [self.section("C", [self.page("Page", "a/b/c/page.md")])])],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_local_recursively(self):
        navigation = self.createAwesomeNavigation(
            [
                self.section(
                    "A",
                    [
                        self.section(
                            "B",
                            [
                                self.section("C", [self.page("Page", "a/b/c/page.md")]),
                                Meta(path="a/b/.pages", collapse_single_pages=True),
                            ],
                        )
                    ],
                )
            ]
        )

        self.assertNavigationEqual(navigation.items, [self.section("A", [self.page("Page", "a/b/c/page.md")])])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_local_recursively_except_current(self):
        navigation = self.createAwesomeNavigation(
            [
                self.section(
                    "A",
                    [
                        self.section(
                            "B",
                            [
                                self.section("C", [self.page("Page", "a/b/c/page.md")]),
                                Meta(
                                    path="a/b/.pages",
                                    collapse_single_pages=True,
                                    collapse=False,
                                ),
                            ],
                        )
                    ],
                )
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [self.section("A", [self.section("B", [self.page("Page", "a/b/c/page.md")])])],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_local_with_hide(self):
        navigation = self.createAwesomeNavigation(
            [
                self.section(
                    "A",
                    [
                        self.section(
                            "B",
                            [
                                self.section("C", [self.page("1", "a/b/c/1.md")]),
                                self.section(
                                    "D",
                                    [
                                        self.page("2", "a/b/d/2.md"),
                                        Meta(path="a/b/d/.pages", hide=True),
                                    ],
                                ),
                                Meta(path="a/b/.pages", collapse=True),
                            ],
                        )
                    ],
                )
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [self.section("A", [self.section("C", [self.page("1", "a/b/c/1.md")])])],
        )
        self.assertValidNavigation(navigation.to_mkdocs())


class TestCollapseGlobalEnabled(NavigationTestCase):
    def test(self):
        navigation = self.createAwesomeNavigation(
            [self.section("Section", [self.page("Page", "section/page.md")])],
            collapse_single_pages=True,
        )

        self.assertNavigationEqual(navigation.items, [self.page("Page", "section/page.md")])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_deep(self):
        navigation = self.createAwesomeNavigation(
            [
                self.section(
                    "A",
                    [self.section("B", [self.section("C", [self.page("1", "a/b/c/1.md")])])],
                ),
                self.section(
                    "E",
                    [
                        self.section(
                            "F",
                            [
                                self.section("G", [self.page("2", "e/f/g/2.md")]),
                                self.page("3", "e/f/3.md"),
                            ],
                        )
                    ],
                ),
            ],
            collapse_single_pages=True,
        )

        self.assertNavigationEqual(
            navigation.items,
            [
                self.page("1", "a/b/c/1.md"),
                self.section("F", [self.page("2", "e/f/g/2.md"), self.page("3", "e/f/3.md")]),
            ],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_override_local(self):
        navigation = self.createAwesomeNavigation(
            [
                self.section(
                    "A",
                    [
                        self.section(
                            "B",
                            [
                                self.section("C", [self.page("Page", "a/b/c/page.md")]),
                                Meta(path="a/b/.pages", collapse=False),
                            ],
                        )
                    ],
                )
            ],
            collapse_single_pages=True,
        )

        self.assertNavigationEqual(navigation.items, [self.section("B", [self.page("Page", "a/b/c/page.md")])])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_override_local_recursively(self):
        navigation = self.createAwesomeNavigation(
            [
                self.section(
                    "A",
                    [
                        self.section(
                            "B",
                            [
                                self.section("C", [self.page("Page", "a/b/c/page.md")]),
                                Meta(path="a/b/.pages", collapse_single_pages=False),
                            ],
                        )
                    ],
                )
            ],
            collapse_single_pages=True,
        )

        self.assertNavigationEqual(
            navigation.items,
            [self.section("B", [self.section("C", [self.page("Page", "a/b/c/page.md")])])],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_links(self):
        navigation = self.createAwesomeNavigation(
            [self.section("Section", [self.page("Page", "section/page.md"), self.link("Link")])],
            collapse_single_pages=True,
        )

        self.assertNavigationEqual(
            navigation.items,
            [self.section("Section", [self.page("Page", "section/page.md"), self.link("Link")])],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_title(self):
        navigation = self.createAwesomeNavigation(
            [
                self.section(
                    "Section",
                    [
                        self.page("Page", "section/page.md"),
                        Meta(path="section/.pages", title="Section Title"),
                    ],
                )
            ],
            collapse_single_pages=True,
        )

        self.assertNavigationEqual(navigation.items, [self.page("Page", "section/page.md")])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_arrange_duplicate(self):
        navigation = self.createAwesomeNavigation(
            [
                self.section(
                    "Section",
                    [
                        self.page("Page", "section/page.md"),
                        Meta(path="section/.pages", arrange=["page.md", "page.md"]),
                    ],
                )
            ],
            collapse_single_pages=True,
        )

        self.assertNavigationEqual(
            navigation.items,
            [
                self.section(
                    "Section",
                    [
                        self.page("Page", "section/page.md"),
                        self.page("Page", "section/page.md"),
                    ],
                )
            ],
        )
        self.assertValidNavigation(navigation.to_mkdocs(), assert_previous_next=False)

    def test_local_with_hide(self):
        navigation = self.createAwesomeNavigation(
            [
                self.section(
                    "A",
                    [
                        self.section(
                            "B",
                            [
                                self.section("C", [self.page("1", "a/b/c/1.md")]),
                                self.section(
                                    "D",
                                    [
                                        self.page("2", "a/b/d/2.md"),
                                        Meta(path="a/b/d/.pages", hide=True),
                                    ],
                                ),
                            ],
                        )
                    ],
                )
            ],
            collapse_single_pages=True,
        )

        self.assertNavigationEqual(navigation.items, [self.page("1", "a/b/c/1.md")])
        self.assertValidNavigation(navigation.to_mkdocs())
