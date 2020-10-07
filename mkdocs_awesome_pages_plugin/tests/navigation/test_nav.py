from .base import NavigationTestCase
from ...meta import Meta, MetaNavItem
from ...navigation import NavEntryNotFound


class TestNav(NavigationTestCase):

    def test_all_listed(self):
        navigation = self.createAwesomeNavigation([
            self.page('1'),
            self.page('2'),
            self.page('3'),
            Meta(nav=[
                MetaNavItem('2.md'),
                MetaNavItem('3.md'),
                MetaNavItem('1.md')
            ])
        ])

        self.assertNavigationEqual(navigation.items, [
            self.page('2'),
            self.page('3'),
            self.page('1')
        ])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_some_listed(self):
        navigation = self.createAwesomeNavigation([
            self.page('1'),
            self.page('2'),
            self.page('3'),
            Meta(nav=[
                MetaNavItem('3.md'),
                MetaNavItem('1.md')
            ])
        ])

        self.assertNavigationEqual(navigation.items, [
            self.page('3'),
            self.page('1')
        ])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_none_listed(self):
        navigation = self.createAwesomeNavigation([
            self.page('1'),
            self.page('2'),
            self.page('3'),
            Meta(nav=[])
        ])

        self.assertNavigationEqual(navigation.items, [])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_rest(self):
        navigation = self.createAwesomeNavigation([
            self.page('1'),
            self.page('2'),
            self.page('3'),
            self.page('4'),
            Meta(nav=[
                MetaNavItem('3.md'),
                Meta.NAV_REST_TOKEN,
                MetaNavItem('1.md')
            ])
        ])

        self.assertNavigationEqual(navigation.items, [
            self.page('3'),
            self.page('2'),
            self.page('4'),
            self.page('1')
        ])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_rest_empty(self):
        navigation = self.createAwesomeNavigation([
            self.page('1'),
            self.page('2'),
            Meta(nav=[
                MetaNavItem('2.md'),
                Meta.NAV_REST_TOKEN,
                MetaNavItem('1.md')
            ])
        ])

        self.assertNavigationEqual(navigation.items, [
            self.page('2'),
            self.page('1')
        ])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_title(self):
        navigation = self.createAwesomeNavigation([
            self.page('1'),
            self.page('2'),
            Meta(nav=[
                MetaNavItem('2.md', 'Title'),
                MetaNavItem('1.md')
            ])
        ])

        self.assertNavigationEqual(navigation.items, [
            self.page('Title', '2.md'),
            self.page('1')
        ])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_existing_link(self):
        navigation = self.createAwesomeNavigation([
            self.page('1'),
            self.page('2'),
            self.link('Link'),
            Meta(nav=[
                MetaNavItem('2.md'),
                MetaNavItem('1.md')
            ])
        ])

        self.assertNavigationEqual(navigation.items, [
            self.page('2'),
            self.page('1')
        ])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_existing_link_rest(self):
        navigation = self.createAwesomeNavigation([
            self.page('1'),
            self.page('2'),
            self.link('Link'),
            Meta(nav=[
                MetaNavItem('2.md'),
                Meta.NAV_REST_TOKEN,
                MetaNavItem('1.md')
            ])
        ])

        self.assertNavigationEqual(navigation.items, [
            self.page('2'),
            self.link('Link'),
            self.page('1')
        ])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_added_link(self):
        navigation = self.createAwesomeNavigation([
            self.page('1'),
            self.page('2'),
            Meta(nav=[
                MetaNavItem('2.md'),
                MetaNavItem('Url', 'Link'),
                MetaNavItem('1.md')
            ])
        ])

        self.assertNavigationEqual(navigation.items, [
            self.page('2'),
            self.link('Link', 'Url'),
            self.page('1')
        ])
        self.assertValidNavigation(navigation.to_mkdocs())

    def test_duplicate_list_item(self):
        navigation = self.createAwesomeNavigation([
            self.page('1'),
            self.page('2'),
            Meta(nav=[
                MetaNavItem('2.md'),
                MetaNavItem('1.md'),
                MetaNavItem('2.md')
            ])
        ])

        self.assertNavigationEqual(navigation.items, [
            self.page('2'),
            self.page('1'),
            self.page('2')
        ])

    def test_duplicate_navigation_item(self):
        navigation = self.createAwesomeNavigation([
            self.page('1'),
            self.page('2a', '2.md'),
            self.page('2b', '2.md'),
            Meta(nav=[
                MetaNavItem('2.md'),
                MetaNavItem('1.md')
            ])
        ])

        self.assertNavigationEqual(navigation.items, [
            self.page('2b', '2.md'),
            self.page('1')
        ])

    def test_sections(self):
        navigation = self.createAwesomeNavigation([
            self.page('1', '1.md'),
            self.page('2', '2.md'),
            self.section('A', [
                self.page('3', 'a/3.md'),
                self.page('4', 'a/4.md')
            ], 'a'),
            self.section('B', [
                self.page('5', 'b/5.md'),
                self.page('6', 'b/6.md')
            ], 'b'),
            Meta(nav=[
                MetaNavItem('a'),
                Meta.NAV_REST_TOKEN,
                MetaNavItem('2.md')
            ])
        ])

        self.assertNavigationEqual(navigation.items, [
            self.section('A', [
                self.page('3', 'a/3.md'),
                self.page('4', 'a/4.md')
            ]),
            self.page('1', '1.md'),
            self.section('B', [
                self.page('5', 'b/5.md'),
                self.page('6', 'b/6.md')
            ]),
            self.page('2', '2.md')
        ])

    def test_custom_section(self):
        navigation = self.createAwesomeNavigation([
            self.page('1', '1.md'),
            self.page('2', '2.md'),
            self.page('3'),
            Meta(nav=[
                MetaNavItem.from_yaml({'a': ['1.md', '2.md']}, context=''),
                Meta.NAV_REST_TOKEN,
            ])
        ])

        self.assertNavigationEqual(navigation.items, [
            self.section('a', [
                self.page('1', '1.md'),
                self.page('2', '2.md')
            ]),
            self.page('3'),
        ])

    def test_not_found(self):
        with self.assertRaises(NavEntryNotFound):
            self.createAwesomeNavigation([
                self.page('1'),
                self.page('2'),
                Meta(nav=[
                    MetaNavItem('1.md'),
                    MetaNavItem('3.md')
                ])
            ])

    def test_not_found_not_strict(self):
        with self.assertWarns(NavEntryNotFound):
            self.createAwesomeNavigation([
                self.page('1'),
                self.page('2'),
                Meta(nav=[
                    MetaNavItem('1.md'),
                    MetaNavItem('3.md')
                ])
            ], strict=False)
