from ...meta import Meta, MetaNavItem, MetaNavRestItem
from .base import NavigationTestCase


class TestOrderAndSort(NavigationTestCase):
    def test_asc(self):
        navigation = self.createAwesomeNavigation(
            [self.page("1"), self.page("2"), self.page("3"), Meta(order=Meta.ORDER_ASC)]
        )

        self.assertNavigationEqual(navigation.items, [self.page("1"), self.page("2"), self.page("3")])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_asc_natural(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("100"),
                self.page("20"),
                self.page("3"),
                Meta(order=Meta.ORDER_ASC, sort_type=Meta.SORT_NATURAL),
            ]
        )

        self.assertNavigationEqual(navigation.items, [self.page("3"), self.page("20"), self.page("100")])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_asc_natural_with_dot_suffix(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("100."),
                self.page("20."),
                self.page("3."),
                Meta(order=Meta.ORDER_ASC, sort_type=Meta.SORT_NATURAL),
            ]
        )

        self.assertNavigationEqual(navigation.items, [self.page("3."), self.page("20."), self.page("100.")])
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

    def test_desc_natural(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("100"),
                self.page("20"),
                self.page("3"),
                Meta(order=Meta.ORDER_DESC, sort_type=Meta.SORT_NATURAL),
            ]
        )

        self.assertNavigationEqual(navigation.items, [self.page("100"), self.page("20"), self.page("3")])
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

    def test_section_asc_natural(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("100"),
                self.page("3"),
                self.section("20", [self.page("a", "2/a.md")], "20"),
                Meta(order=Meta.ORDER_ASC, sort_type=Meta.SORT_NATURAL),
            ]
        )
        self.assertNavigationEqual(
            navigation.items,
            [
                self.page("3"),
                self.section("20", [self.page("a", "2/a.md")], "20"),
                self.page("100"),
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

    def test_section_desc_natural(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("100"),
                self.page("3"),
                self.section("20", [self.page("a", "2/a.md")], "20"),
                Meta(order=Meta.ORDER_DESC, sort_type=Meta.SORT_NATURAL),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [
                self.page("100"),
                self.section("20", [self.page("a", "2/a.md")], "20"),
                self.page("3"),
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

    def test_nav_asc_natural(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("100"),
                self.page("20"),
                self.page("3"),
                Meta(
                    order=Meta.ORDER_ASC,
                    sort_type=Meta.SORT_NATURAL,
                    nav=[MetaNavItem("20.md"), MetaNavItem("3.md"), MetaNavItem("100.md")],
                ),
            ]
        )

        self.assertNavigationEqual(navigation.items, [self.page("20"), self.page("3"), self.page("100")])
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

    def test_nav_desc_natural(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("100"),
                self.page("20"),
                self.page("3"),
                Meta(
                    order=Meta.ORDER_DESC,
                    sort_type=Meta.SORT_NATURAL,
                    nav=[MetaNavItem("20.md"), MetaNavItem("3.md"), MetaNavItem("100.md")],
                ),
            ]
        )

        self.assertNavigationEqual(navigation.items, [self.page("20"), self.page("3"), self.page("100")])
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

    def test_nav_rest_asc_natural(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1000"),
                self.page("200"),
                self.page("30"),
                self.page("4"),
                Meta(
                    order=Meta.ORDER_ASC,
                    sort_type=Meta.SORT_NATURAL,
                    nav=[MetaNavItem("30.md"), MetaNavRestItem("...")],
                ),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [self.page("30"), self.page("4"), self.page("200"), self.page("1000")],
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

    def test_nav_rest_desc_natural(self):
        navigation = self.createAwesomeNavigation(
            [
                self.page("1000"),
                self.page("200"),
                self.page("30"),
                self.page("4"),
                Meta(
                    order=Meta.ORDER_DESC,
                    sort_type=Meta.SORT_NATURAL,
                    nav=[MetaNavItem("30.md"), MetaNavRestItem("...")],
                ),
            ]
        )

        self.assertNavigationEqual(
            navigation.items,
            [self.page("30"), self.page("1000"), self.page("200"), self.page("4")],
        )
        self.assertValidNavigation(navigation.to_mkdocs())
