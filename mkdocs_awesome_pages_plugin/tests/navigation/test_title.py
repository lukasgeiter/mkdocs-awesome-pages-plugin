from ...meta import Meta
from ...navigation import TitleInRootHasNoEffect
from .base import NavigationTestCase


class TestTitle(NavigationTestCase):
    def test(self):
        navigation = self.createAwesomeNavigation(
            [
                self.section(
                    "Section",
                    [
                        self.page("Page", "section/page.md"),
                        Meta(path="section/.pages", title="Section Title"),
                    ],
                )
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [self.section("Section Title", [self.page("Page", "section/page.md")])],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_in_root(self):
        with self.assertWarns(TitleInRootHasNoEffect):
            navigation = self.createAwesomeNavigation(
                [self.page("Page", "page.md"), Meta(path=".pages", title="Root Title")]
            )

        self.assertNavigationEqual(navigation.items, [self.page("Page", "page.md")])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_deep(self):
        navigation = self.createAwesomeNavigation(
            [
                self.section(
                    "A",
                    [
                        self.section(
                            "B",
                            [
                                self.page("Page", "a/b/page.md"),
                                Meta(path="a/b/.pages", title="Section B Title"),
                            ],
                        ),
                        Meta(path="s1/.pages", title="Section A Title"),
                    ],
                )
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [
                self.section(
                    "Section A Title",
                    [self.section("Section B Title", [self.page("Page", "a/b/page.md")])],
                )
            ],
        )
        self.assertValidNavigation(navigation.to_mkdocs())
