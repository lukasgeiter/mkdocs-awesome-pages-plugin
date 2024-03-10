from ...meta import Meta
from ...navigation import NavEntryNotFound
from .base import NavigationTestCase


class TestArrange(NavigationTestCase):
    def test(self):
        navigation = self.createAwesomeNavigation(
            [
                self.section(
                    "Section",
                    [
                        self.page("1", "section/1.md"),
                        self.page("2", "section/2.md"),
                        self.page("3", "section/3.md"),
                        Meta(path="section/.pages", arrange=["2.md", "...", "1.md"]),
                    ],
                )
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [
                self.section(
                    "Section",
                    [
                        self.page("2", "section/2.md"),
                        self.page("3", "section/3.md"),
                        self.page("1", "section/1.md"),
                    ],
                )
            ],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_in_root(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1", "1.md"),
                self.page("2", "2.md"),
                self.page("3", "3.md"),
                Meta(path=".pages", arrange=["2.md", "...", "1.md"]),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [self.page("2", "2.md"), self.page("3", "3.md"), self.page("1", "1.md")],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_sections(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1", "1.md"),
                self.page("2", "2.md"),
                self.section("A", [self.page("3", "a/3.md"), self.page("4", "a/4.md")], "a"),
                self.section("B", [self.page("5", "b/5.md"), self.page("6", "b/6.md")], "b"),
                Meta(path=".pages", arrange=["a", "...", "2.md"]),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [
                self.section("A", [self.page("3", "a/3.md"), self.page("4", "a/4.md")]),
                self.page("1", "1.md"),
                self.section("B", [self.page("5", "b/5.md"), self.page("6", "b/6.md")]),
                self.page("2", "2.md"),
            ],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_deep(self):
        navigation = self.createAwesomeNavigation(
            [
                self.section(
                    "A",
                    [
                        self.page("1", "a/1.md"),
                        self.page("2", "a/2.md"),
                        self.page("3", "a/3.md"),
                        Meta(path="a/.pages", arrange=["...", "1.md"]),
                    ],
                ),
                self.section(
                    "B",
                    [
                        self.page("4", "b/4.md"),
                        self.page("5", "b/5.md"),
                        self.page("6", "b/6.md"),
                        Meta(path="b/.pages", arrange=["5.md"]),
                    ],
                ),
                Meta(path=".pages", arrange=["b", "a"]),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [
                self.section(
                    "B",
                    [
                        self.page("5", "b/5.md"),
                        self.page("4", "b/4.md"),
                        self.page("6", "b/6.md"),
                    ],
                ),
                self.section(
                    "A",
                    [
                        self.page("2", "a/2.md"),
                        self.page("3", "a/3.md"),
                        self.page("1", "a/1.md"),
                    ],
                ),
            ],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_links(self):
        navigation = self.createAwesomeNavigation(
            [
                self.link("Link 1"),
                self.page("Page 1", "1.md"),
                self.link("Link 2"),
                self.page("Page 2", "2.md"),
                Meta(path=".pages", arrange=["2.md"]),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [
                self.page("Page 2", "2.md"),
                self.link("Link 1"),
                self.page("Page 1", "1.md"),
                self.link("Link 2"),
            ],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_collapsed(self):
        navigation = self.createAwesomeNavigation(
            [
                self.section("A", [self.page("1", "a/1.md"), self.page("2", "a/2.md")], "a"),
                self.section("B", [self.page("3", "b/3.md")], "b"),
                Meta(path=".pages", arrange=["b", "a"]),
            ],
            collapse_single_pages=True,
        )

        self.assertNavigationEqual(
            navigation.items,
            [
                self.page("3", "b/3.md"),
                self.section("A", [self.page("1", "a/1.md"), self.page("2", "a/2.md")]),
            ],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_duplicates(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1", "1.md"),
                self.page("2", "2.md"),
                self.page("3", "3.md"),
                Meta(path=".pages", arrange=["2.md", "2.md", "3.md", "1.md", "3.md"]),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [
                self.page("2", "2.md"),
                self.page("2", "2.md"),
                self.page("3", "3.md"),
                self.page("1", "1.md"),
                self.page("3", "3.md"),
            ],
        )
        mkdocs_navigation = navigation.to_mkdocs()
        self.assertValidNavigation(mkdocs_navigation, assert_previous_next=False)

        # the previous and next links have to be asserted manually
        # because duplicate navigation entries are two references to the same object
        page1 = mkdocs_navigation.pages[3]
        page2 = mkdocs_navigation.pages[0]
        self.assertEqual(mkdocs_navigation.pages[1], page2)
        page3 = mkdocs_navigation.pages[2]
        self.assertEqual(mkdocs_navigation.pages[4], page3)

        self.assertEqual(page2.previous_page, page2)
        self.assertEqual(page2.next_page, page3)

        self.assertEqual(page3.previous_page, page1)
        self.assertEqual(page3.next_page, None)

        self.assertEqual(page1.previous_page, page3)
        self.assertEqual(page1.next_page, page3)

    def test_entry_not_found(self):
        with self.assertRaises(NavEntryNotFound):
            self.createAwesomeNavigation(
                [
                    self.page("1", "1.md"),
                    self.page("2", "2.md"),
                    Meta(path=".pages", arrange=["1.md", "...", "3.md"]),
                ]
            )

    def test_entry_not_found_not_strict(self):
        with self.assertWarns(NavEntryNotFound):
            self.createAwesomeNavigation(
                [
                    self.page("1", "1.md"),
                    self.page("2", "2.md"),
                    Meta(path=".pages", arrange=["1.md", "...", "3.md"]),
                ],
                strict=False,
            )
