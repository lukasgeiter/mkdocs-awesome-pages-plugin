from .base import E2ETestCase
from ...meta import DuplicateRestTokenError
from ...navigation import NavEntryNotFound


class TestNav(E2ETestCase):

    def test_all_listed(self):
        navigation = self.mkdocs(self.config, [
            '1.md',
            '2.md',
            ('a', [
                '1.md',
                '2.md',
                self.pagesFile(nav=[
                    '2.md',
                    '1.md'
                ])
            ]),
            self.pagesFile(nav=[
                'a',
                '2.md',
                '1.md'
            ])
        ])

        self.assertEqual(navigation, [
            ('A', [
                ('2', '/a/2'),
                ('1', '/a/1')
            ]),
            ('2', '/2'),
            ('1', '/1')
        ])

    def test_some_listed(self):
        navigation = self.mkdocs(self.config, [
            '1.md',
            '2.md',
            ('a', [
                '1.md',
                '2.md',
                self.pagesFile(nav=[
                    '1.md'
                ])
            ]),
            self.pagesFile(nav=[
                'a',
                '1.md'
            ])
        ])

        self.assertEqual(navigation, [
            ('A', [
                ('1', '/a/1')
            ]),
            ('1', '/1')
        ])

    def test_none_listed(self):
        navigation = self.mkdocs(self.config, [
            '1.md',
            ('a', [
                '1.md',
                '2.md',
                self.pagesFile(nav=[])
            ])
        ])

        self.assertEqual(navigation, [
            ('1', '/1')
        ])

    def test_rest(self):
        navigation = self.mkdocs(self.config, [
            '1.md',
            '2.md',
            ('a', [
                '1.md',
                '2.md',
                '3.md',
                '4.md',
                self.pagesFile(nav=[
                    '2.md',
                    '...',
                    '1.md'
                ])
            ]),
            self.pagesFile(nav=[
                '2.md',
                '...'
            ])
        ])

        self.assertEqual(navigation, [
            ('2', '/2'),
            ('1', '/1'),
            ('A', [
                ('2', '/a/2'),
                ('3', '/a/3'),
                ('4', '/a/4'),
                ('1', '/a/1')
            ])
        ])

    def test_rest_empty(self):
        navigation = self.mkdocs(self.config, [
            '1.md',
            ('a', [
                '1.md',
                '2.md',
                self.pagesFile(nav=[
                    '2.md',
                    '...',
                    '1.md'
                ])
            ]),
            self.pagesFile(nav=[
                'a',
                '...',
                '1.md'
            ])
        ])

        self.assertEqual(navigation, [
            ('A', [
                ('2', '/a/2'),
                ('1', '/a/1')
            ]),
            ('1', '/1')
        ])

    def test_title(self):
        navigation = self.mkdocs(self.config, [
            '1.md',
            '2.md',
            ('a', [
                '1.md',
                '2.md',
                self.pagesFile(nav=[
                    '1.md',
                    {'Title 2': '2.md'}
                ])
            ]),
            self.pagesFile(nav=[
                {'Title 1': '1.md'},
                '2.md',
                {'Title A': 'a'}
            ])
        ])

        self.assertEqual(navigation, [
            ('Title 1', '/1'),
            ('2', '/2'),
            ('Title A', [
                ('1', '/a/1'),
                ('Title 2', '/a/2')
            ])
        ])

    def test_title_conflict(self):
        navigation = self.mkdocs(self.config, [
            ('a', [
                '1.md',
                '2.md',
                self.pagesFile(title='Title Meta')
            ]),
            self.pagesFile(nav=[
                {'Title Nav': 'a'},
                '...'
            ])
        ])

        self.assertEqual(navigation, [
            ('Title Meta', [
                ('1', '/a/1'),
                ('2', '/a/2')
            ])
        ])

    def test_link(self):
        navigation = self.mkdocs(self.config, [
            '1.md',
            ('a', [
                '1.md',
                self.pagesFile(nav=[
                    '...',
                    {'Internal Link': '/link'},
                    {'External Link': 'https://lukasgeiter.com'}
                ])
            ]),
            self.pagesFile(nav=[
                '...',
                {'Internal Link': '/link'},
                {'External Link': 'https://lukasgeiter.com'}
            ])
        ])

        self.assertEqual(navigation, [
            ('1', '/1'),
            ('A', [
                ('1', '/a/1'),
                ('Internal Link', '/link'),
                ('External Link', 'https://lukasgeiter.com')
            ]),
            ('Internal Link', '/link'),
            ('External Link', 'https://lukasgeiter.com')
        ])

    def test_collapsed(self):
        navigation = self.mkdocs(self.createConfig(collapse_single_pages=True), [
            ('a', [
                '1.md',
                '2.md'
            ]),
            ('b', [
                '1.md'
            ]),
            self.pagesFile(arrange=[
                'b',
                'a'
            ])
        ])

        self.assertEqual(navigation, [
            ('1', '/b/1'),
            ('A', [
                ('1', '/a/1'),
                ('2', '/a/2')
            ])
        ])

    def test_duplicate_file(self):
        navigation = self.mkdocs(self.createConfig(mkdocs_nav=[
            {'1a': '1.md'},
            {'2': '2.md'},
            {'1b': '1.md'}
        ]), [
            '1.md',
            '2.md',
            self.pagesFile(nav=[
                '2.md',
                '1.md'
            ])
        ])

        self.assertEqual(navigation, [
            ('2', '/2'),
            ('1b', '/1')
        ])

    def test_duplicate_file_rest(self):
        navigation = self.mkdocs(self.createConfig(mkdocs_nav=[
            {'1a': '1.md'},
            {'2': '2.md'},
            {'1b': '1.md'}
        ]), [
            '1.md',
            '2.md',
            self.pagesFile(nav=[
                '2.md',
                '...'
            ])
        ])

        self.assertEqual(navigation, [
            ('2', '/2'),
            ('1a', '/1'),
            ('1b', '/1')
        ])

    def test_duplicate_entry(self):
        navigation = self.mkdocs(self.config, [
            '1.md',
            ('a', [
                '1.md',
                '2.md',
                self.pagesFile(nav=[
                    '2.md',
                    '...',
                    '2.md'
                ])
            ]),
            self.pagesFile(nav=[
                'a',
                '...',
                'a'
            ])
        ])

        self.assertEqual(navigation, [
            ('A', [
                ('2', '/a/2'),
                ('1', '/a/1'),
                ('2', '/a/2')
            ]),
            ('1', '/1'),
            ('A', [
                ('2', '/a/2'),
                ('1', '/a/1'),
                ('2', '/a/2')
            ])
        ])

    def test_duplicate_entry_title(self):
        navigation = self.mkdocs(self.config, [
            '1.md',
            ('a', [
                '1.md',
                '2.md',
                self.pagesFile(nav=[
                    {'2a': '2.md'},
                    '...',
                    {'2b': '2.md'}
                ])
            ]),
            self.pagesFile(nav=[
                {'AA': 'a'},
                '...',
                {'AB': 'a'}
            ])
        ])

        self.assertEqual(navigation, [
            ('AB', [
                ('2b', '/a/2'),
                ('1', '/a/1'),
                ('2b', '/a/2')
            ]),
            ('1', '/1'),
            ('AB', [
                ('2b', '/a/2'),
                ('1', '/a/1'),
                ('2b', '/a/2')
            ])
        ])

    def test_duplicate_rest_token(self):
        with self.assertRaises(DuplicateRestTokenError):
            self.mkdocs(self.config, [
                '1.md',
                '2.md',
                self.pagesFile(nav=[
                    '...',
                    '1.md',
                    '...'
                ])
            ])

    def test_not_found(self):
        with self.assertRaises(NavEntryNotFound):
            self.mkdocs(self.config, [
                self.pagesFile(nav=[
                    '1.md',
                    '...'
                ])
            ])

    def test_not_found_strict(self):
        with self.assertRaises(NavEntryNotFound):
            self.mkdocs(self.createConfig(strict=True), [
                self.pagesFile(nav=[
                    '1.md',
                    '...'
                ])
            ])

    def test_not_found_not_strict(self):
        with self.assertWarns(NavEntryNotFound):
            self.mkdocs(self.createConfig(strict=False), [
                self.pagesFile(nav=[
                    '1.md',
                    '...'
                ])
            ])
