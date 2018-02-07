from unittest import TestCase

from ..page import Page, RootPage


class TestPage(TestCase):

    def test_basename_path_none(self):
        page = Page('Foo', None)
        self.assertIsNone(page.basename)

    def test_basename(self):
        page = Page('Foo', 'foo/foo.md')
        self.assertEqual(page.basename, 'foo.md')

    def test_dirname_path_none(self):
        page = Page('Foo', None)
        self.assertIsNone(page.dirname)

    def test_dirname(self):
        page = Page('Foo', 'foo/foo.md')
        self.assertEqual(page.dirname, 'foo')

    def test_to_mkdocs(self):
        page = Page('Foo', 'foo.md')
        self.assertEqual(page.to_mkdocs(), {
            'Foo': 'foo.md'
        })

    def test_to_mkdocs_no_title(self):
        page = Page(None, 'foo.md')
        self.assertEqual(page.to_mkdocs(), 'foo.md')

    def test_to_mkdocs_root(self):
        page = RootPage([
            Page('Foo', 'foo.md'),
            Page('Bar', 'bar.md')
        ])
        self.assertEqual(page.to_mkdocs(), [
            {
                'Foo': 'foo.md'
            },
            {
                'Bar': 'bar.md'
            }
        ])

    def test_to_mkdocs_empty_root(self):
        page = RootPage([])
        self.assertEqual(page.to_mkdocs(), [])

    def test_to_mkdocs_tree(self):
        tree = RootPage([
            Page('Foo', 'foo.md'),
            Page('Bar', 'bar', [
                Page(None, 'bar/index.md'),
                Page('BarBar', 'bar/bar.md')
            ])
        ])
        self.assertEqual(tree.to_mkdocs(), [
            {
                'Foo': 'foo.md'
            },
            {
                'Bar': [
                    'bar/index.md',
                    {
                        'BarBar': 'bar/bar.md'
                    }
                ]
            }
        ])
