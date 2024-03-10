from ...meta import Meta
from ...navigation import HideInRootHasNoEffect
from .base import NavigationTestCase


class TestHide(NavigationTestCase):
    def test(self):
        navigation = self.createAwesomeNavigation(
            [
                self.section("A", [self.page("1", "a/1.md"), Meta(path="a/.pages", hide=True)]),
                self.section("B", [self.page("2", "b/2.md")]),
            ]
        )

        self.assertNavigationEqual(navigation.items, [self.section("B", [self.page("2", "b/2.md")])])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_single_root_section(self):
        navigation = self.createAwesomeNavigation(
            [
                self.section(
                    "Section",
                    [
                        self.page("Page", "section/1.md"),
                        Meta(path="section/.pages", hide=True),
                    ],
                )
            ]
        )

        self.assertNavigationEqual(navigation.items, [])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_propagate(self):
        navigation = self.createAwesomeNavigation(
            [
                self.section(
                    "A",
                    [
                        self.section(
                            "B",
                            [
                                self.page("Page", "a/b/page.md"),
                                Meta(path="a/b/.pages", hide=True),
                            ],
                        )
                    ],
                )
            ]
        )

        self.assertNavigationEqual(navigation.items, [])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_propagate_deep(self):
        navigation = self.createAwesomeNavigation(
            [
                self.section(
                    "A",
                    [
                        self.section(
                            "B",
                            [
                                self.section(
                                    "C",
                                    [
                                        self.page("1", "a/b/c/1.md"),
                                        Meta(path="a/b/c/.pages", hide=True),
                                    ],
                                )
                            ],
                        ),
                        self.section("D", [self.page("2", "a/d/2.md")]),
                    ],
                )
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [self.section("A", [self.section("D", [self.page("2", "a/d/2.md")])])],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_in_root(self):
        with self.assertWarns(HideInRootHasNoEffect):
            navigation = self.createAwesomeNavigation([self.page("Page", "page.md"), Meta(path=".pages", hide=True)])

        self.assertNavigationEqual(navigation.items, [self.page("Page", "page.md")])
        self.assertValidNavigation(navigation.to_mkdocs())
