from .base import NavigationTestCase
from ...meta import Meta, MetaNavItem, MetaNavRestItem


class TestOrder(NavigationTestCase):
    def test_asc(self):
        navigation = self.createAwesomeNavigation(
            [self.page("1"), self.page("2"), self.page("3"), Meta(order=Meta.ORDER_ASC)]
        )

        self.assertNavigationEqual(navigation.items, [self.page("1"), self.page("2"), self.page("3")])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_desc(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("2"),
                self.page("3"),
                Meta(order=Meta.ORDER_DESC),
            ]
        )

        self.assertNavigationEqual(navigation.items, [self.page("3"), self.page("2"), self.page("1")])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_section_asc(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("3"),
                self.section("2", [self.page("a", "2/a.md")], "2"),
                Meta(order=Meta.ORDER_ASC),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [
                self.page("1"),
                self.section("2", [self.page("a", "2/a.md")], "2"),
                self.page("3"),
            ],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_section_desc(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("3"),
                self.section("2", [self.page("a", "2/a.md")], "2"),
                Meta(order=Meta.ORDER_DESC),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [
                self.page("3"),
                self.section("2", [self.page("a", "2/a.md")], "2"),
                self.page("1"),
            ],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_nav_asc(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("2"),
                self.page("3"),
                Meta(
                    order=Meta.ORDER_ASC,
                    nav=[MetaNavItem("2.md"), MetaNavItem("3.md"), MetaNavItem("1.md")],
                ),
            ]
        )

        self.assertNavigationEqual(navigation.items, [self.page("2"), self.page("3"), self.page("1")])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_nav_desc(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("2"),
                self.page("3"),
                Meta(
                    order=Meta.ORDER_DESC,
                    nav=[MetaNavItem("2.md"), MetaNavItem("3.md"), MetaNavItem("1.md")],
                ),
            ]
        )

        self.assertNavigationEqual(navigation.items, [self.page("2"), self.page("3"), self.page("1")])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_nav_rest_asc(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("2"),
                self.page("3"),
                self.page("4"),
                Meta(
                    order=Meta.ORDER_ASC,
                    nav=[MetaNavItem("4.md"), MetaNavRestItem("...")],
                ),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [self.page("4"), self.page("1"), self.page("2"), self.page("3")],
        )
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_nav_rest_desc(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1"),
                self.page("2"),
                self.page("3"),
                self.page("4"),
                Meta(
                    order=Meta.ORDER_DESC,
                    nav=[MetaNavItem("1.md"), MetaNavRestItem("...")],
                ),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [self.page("1"), self.page("4"), self.page("3"), self.page("2")],
        )
        self.assertValidNavigation(navigation.to_mkdocs())
