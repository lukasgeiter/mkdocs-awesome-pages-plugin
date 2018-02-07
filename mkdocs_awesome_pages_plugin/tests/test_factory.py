import os
from unittest import mock, TestCase
from .file_mock import FileMock

from ..pagesfile import PagesFile
from ..page import Page
from ..factory import Factory, PageNotFoundError, TitleInRootPagesFileWarning


@mock.patch('builtins.open', new_callable=FileMock)
class TestCreate(TestCase):

    def setUp(self):
        self.factory = Factory(
            filename='.pages',
            disable_auto_arrange_index=False
        )

    def test_one_level(self, file_mock: FileMock):
        config = [
            {
                'Foo': 'foo.md'
            },
            {
                'Bar': 'bar.md'
            }
        ]
        tree = self.factory.create(config)

        self.assertIsNone(tree.title)
        self.assertEqual(tree.path, '')

        self.assertEqual(tree.children[0].title, 'Foo')
        self.assertEqual(tree.children[0].path, 'foo.md')

        self.assertEqual(tree.children[1].title, 'Bar')
        self.assertEqual(tree.children[1].path, 'bar.md')

        self.assertEqual(tree.to_config(), config)

    def test_two_levels(self, file_mock: FileMock):
        config = [
            {
                'Foo': 'foo.md'
            },
            {
                'Bar': [
                    {
                        'BarFoo': 'bar/foo.md'
                    },
                    {
                        'BarBar': 'bar/bar.md'
                    }
                ]
            }
        ]
        tree = self.factory.create(config)

        self.assertIsNone(tree.title)
        self.assertEqual(tree.path, '')

        self.assertEqual(tree.children[0].title, 'Foo')
        self.assertEqual(tree.children[0].path, 'foo.md')

        self.assertEqual(tree.children[1].title, 'Bar')
        self.assertEqual(tree.children[1].path, 'bar')

        self.assertEqual(tree.children[1].children[0].title, 'BarFoo')
        self.assertEqual(tree.children[1].children[0].path, 'bar/foo.md')

        self.assertEqual(tree.children[1].children[1].title, 'BarBar')
        self.assertEqual(tree.children[1].children[1].path, 'bar/bar.md')

        self.assertEqual(tree.to_config(), config)

    def test_pages_file_in_root_title(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'title: Root\n'
        )

        with self.assertWarns(TitleInRootPagesFileWarning):
            self.factory.create([])

    def test_pages_file_in_root_arrange(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'arrange:\n'
            '  - foo.md\n'
            '  - bar.md\n'
        )

        config = [
            'bar.md',
            'foo.md'
        ]

        tree = self.factory.create(config)

        self.assertIsNone(tree.title)
        self.assertEqual(tree.path, '')

        self.assertIsNone(tree.children[0].title)
        self.assertEqual(tree.children[0].path, 'foo.md')

        self.assertIsNone(tree.children[1].title)
        self.assertEqual(tree.children[1].path, 'bar.md')

    def test_example(self, file_mock: FileMock):
        file_mock[os.path.join('bar', '.pages')].read_data = (
            'title: Bar Title\n'
            'arrange:\n'
            '  - index.md\n'
            '  - ...\n'
            '  - foo\n'
        )

        file_mock['bar/bar.md'].read_data = (
            '# Bar Bar Title\n'
            '\n'
            'Lorem ipsum dolor sit amet\n'
        )

        file_mock[os.path.join('foo', '.pages')].read_data = (
            'title: Foo Index Title\n'  # is not supposed to be used
        )

        config = [
            {
                'Bar': [
                    {
                        'BarFoo': [
                            {
                                'BarFoo': 'bar/foo/index.md'
                            },
                            {
                                'BarFooBar': 'bar/foo/bar.md'
                            }
                        ]
                    },
                    'bar/foo.md',
                    'bar/bar.md',
                    'bar/index.md'
                ]
            },
            {
                'Foo': [
                    {
                        'FooBar': [
                            'foo/foo/foo.md',
                            'foo/bar/index.md'
                        ]
                    },
                    {
                        'Index': 'foo/index.md'
                    }
                ]
            },
            {
                'Home': 'index.md'
            }
        ]

        self.assertEqual(self.factory.create(config).to_config(), [
            {
                'Home': 'index.md'
            },
            {
                'Bar Title': [
                    'bar/index.md',
                    'bar/foo.md',
                    {
                        'Bar Bar Title': 'bar/bar.md'
                    },
                    {
                        'BarFoo': [
                            {
                                'BarFoo': 'bar/foo/index.md'
                            },
                            {
                                'BarFooBar': 'bar/foo/bar.md'
                            }
                        ]
                    }
                ]
            },
            {
                'Foo': [
                    {
                        'Index': 'foo/index.md'
                    },
                    {
                        'FooBar': [
                            'foo/bar/index.md',
                            'foo/foo/foo.md'
                        ]
                    }
                ]
            },
        ])


@mock.patch('builtins.open', new_callable=FileMock)
class TestCreatePage(TestCase):

    def setUp(self):
        self.factory = Factory(
            filename='.pages',
            disable_auto_arrange_index=False
        )

    def test_leaf_page(self, file_mock: FileMock):
        page = self.factory.create_page({
            'Foo': 'foo.md'
        })
        self.assertEqual(page.title, 'Foo')
        self.assertEqual(page.path, 'foo.md')

    def test_leaf_page_without_title(self, file_mock: FileMock):
        page = self.factory.create_page('foo.md')
        self.assertIsNone(page.title)
        self.assertEqual(page.path, 'foo.md')

    def test_leaf_page_extracted_title(self, file_mock: FileMock):
        file_mock['foo.md'].read_data = (
            '# Foo title\n'
        )

        page = self.factory.create_page({
            'Foo': 'foo.md'
        })
        self.assertEqual(page.title, 'Foo title')
        self.assertEqual(page.path, 'foo.md')

    def test_leaf_page_without_title_extracted_title(self, file_mock: FileMock):
        file_mock['foo.md'].read_data = (
            '# Foo title\n'
        )

        page = self.factory.create_page('foo.md')
        self.assertEqual(page.title, 'Foo title')
        self.assertEqual(page.path, 'foo.md')

    def test_branch_page(self, file_mock: FileMock):
        page = self.factory.create_page({
            'Foo': [
                {
                    'Bar': 'foo/bar.md'
                }
            ]
        })
        self.assertEqual(page.title, 'Foo')
        self.assertEqual(page.path, 'foo')
        self.assertEqual(len(page.children), 1)

    def test_branch_page_without_children(self, file_mock: FileMock):
        page = self.factory.create_page({
            'Foo': []
        })
        self.assertEqual(page.title, 'Foo')
        self.assertIsNone(page.path)
        self.assertEqual(len(page.children), 0)

    def test_branch_page_without_common_dirname(self, file_mock: FileMock):
        page = self.factory.create_page({
            'Foo': [
                'foo/foo.md',
                'bar/bar.md'
            ]
        })
        self.assertEqual(page.title, 'Foo')
        self.assertIsNone(page.path)
        self.assertEqual(len(page.children), 2)

    def test_branch_page_with_path_none_child(self, file_mock: FileMock):
        page = self.factory.create_page({
            'Foo': [
                'foo/foo.md',
                {
                    'Bar': [
                        'foo/foo/foo.md',
                        'foo/bar/bar.md'
                    ]
                }
            ]
        })
        self.assertEqual(page.title, 'Foo')
        self.assertIsNone(page.path)
        self.assertEqual(len(page.children), 2)

    def test_branch_page_with_duplicate_path_children(self, file_mock: FileMock):
        page = self.factory.create_page({
            'Foo': [
                'foo/foo.md',
                'foo/foo.md'
            ]
        })
        self.assertEqual(page.title, 'Foo')
        self.assertEqual(page.path, 'foo')
        self.assertEqual(len(page.children), 2)

    def test_branch_page_title(self, file_mock: FileMock):
        file_mock[os.path.join('foo', '.pages')].read_data = (
            'title: Foo title\n'
        )

        page = self.factory.create_page({
            'Foo': [
                {
                    'Bar': 'foo/bar.md'
                }
            ]
        })
        self.assertEqual(page.title, 'Foo title')
        self.assertEqual(page.path, 'foo')

    def test_branch_page_arrange(self, file_mock: FileMock):
        file_mock[os.path.join('foo', '.pages')].read_data = (
            'arrange:\n'
            '  - foo.md\n'
            '  - bar.md\n'
        )

        page = self.factory.create_page({
            'Foo': [
                'foo/bar.md',
                'foo/foo.md'
            ]
        })
        self.assertEqual(page.title, 'Foo')
        self.assertEqual(page.children[0].path, 'foo/foo.md')
        self.assertEqual(page.children[1].path, 'foo/bar.md')

    def test_branch_pages_filename_option(self, file_mock: FileMock):
        self.factory.options.filename = '.index'

        file_mock[os.path.join('foo', '.index')].read_data = (
            'title: Foo title\n'
        )

        page = self.factory.create_page({
            'Foo': [
                {
                    'Bar': 'foo/bar.md'
                }
            ]
        })
        self.assertEqual(page.title, 'Foo title')
        self.assertEqual(page.path, 'foo')


class TestCommonDirname(TestCase):
    def setUp(self):
        self.factory = Factory(
            filename='.pages',
            disable_auto_arrange_index=False
        )

    def test_same_common_dirname(self):
        dirname = self.factory.common_dirname([
            Page('Foo', 'common/foo.md'),
            Page('Bar', 'common/bar.md')
        ])
        self.assertEqual(dirname, 'common')

    def test_same_common_dirname_multi_level(self):
        dirname = self.factory.common_dirname([
            Page('Foo', 'multi/level/common/foo.md'),
            Page('Bar', 'multi/level/common/bar.md')
        ])
        self.assertEqual(dirname, 'multi/level/common')

    def test_different_dirname(self):
        dirname = self.factory.common_dirname([
            Page('Foo', 'common/foo/foo.md'),
            Page('Bar', 'common/bar/bar.md')
        ])
        self.assertIsNone(dirname)

    def test_path_none(self):
        dirname = self.factory.common_dirname([
            Page('Foo', 'common/foo.md'),
            Page('Bar', 'common/bar.md'),
            Page('None', None)
        ])
        self.assertIsNone(dirname)

    def test_first_path_none(self):
        dirname = self.factory.common_dirname([
            Page('None', None),
            Page('Foo', 'common/foo.md'),
            Page('Bar', 'common/bar.md')
        ])
        self.assertIsNone(dirname)

    def test_no_directory(self):
        dirname = self.factory.common_dirname([
            Page('Foo', 'foo.md'),
            Page('Bar', 'bar.md')
        ])
        self.assertEqual(dirname, '')

    def test_one_page(self):
        dirname = self.factory.common_dirname([
            Page('Foo', 'common/foo.md')
        ])
        self.assertEqual(dirname, 'common')

    def test_no_pages(self):
        self.assertIsNone(self.factory.common_dirname([]))


class TestArrangePages(TestCase):
    def setUp(self):
        self.factory = Factory(
            filename='.pages',
            disable_auto_arrange_index=False
        )

    def test_no_pages_no_pages_file(self):
        self.assertEqual(self.factory.arrange_pages([], PagesFile()), [])

    def test_no_pages_file(self):
        pages = [
            Page('Foo', 'foo.md'),
            Page('Bar', 'bar.md')
        ]
        self.assertEqual(self.factory.arrange_pages(pages, PagesFile()), pages)

    def test_one_in_pages_file(self):
        foo = Page('Foo', 'foo.md')
        bar = Page('Bar', 'bar.md')
        index = Page('Index', 'index.md')
        pages = [
            foo, bar, index
        ]
        self.assertEqual(self.factory.arrange_pages(pages, PagesFile(arrange=[
            'bar.md'
        ])), [
            bar, foo, index
        ])

    def test_all_in_pages_file(self):
        foo = Page('Foo', 'foo.md')
        bar = Page('Bar', 'bar.md')
        baz = Page('Baz', 'baz.md')
        pages = [
            foo, bar, baz
        ]
        self.assertEqual(self.factory.arrange_pages(pages, PagesFile(arrange=[
            'baz.md',
            'bar.md',
            'foo.md'
        ])), [
            baz, bar, foo
        ])

    def test_rest_token_beginning(self):
        foo = Page('Foo', 'foo.md')
        bar = Page('Bar', 'bar.md')
        baz = Page('Baz', 'baz.md')
        pages = [
            foo, bar, baz
        ]
        self.assertEqual(self.factory.arrange_pages(pages, PagesFile(arrange=[
            '...',
            'bar.md'
        ])), [
            foo, baz, bar
        ])

    def test_rest_token_middle(self):
        foo = Page('Foo', 'foo.md')
        bar = Page('Bar', 'bar.md')
        baz = Page('Baz', 'baz.md')
        pages = [
            foo, bar, baz
        ]
        self.assertEqual(self.factory.arrange_pages(pages, PagesFile(arrange=[
            'baz.md',
            '...',
            'bar.md'
        ])), [
            baz, foo, bar
        ])

    def test_rest_token_end(self):
        foo = Page('Foo', 'foo.md')
        bar = Page('Bar', 'bar.md')
        baz = Page('Baz', 'baz.md')
        pages = [
            foo, bar, baz
        ]
        self.assertEqual(self.factory.arrange_pages(pages, PagesFile(arrange=[
            'bar.md',
            '...'
        ])), [
            bar, foo, baz
        ])

    def test_rest_token_no_rest(self):
        foo = Page('Foo', 'foo.md')
        bar = Page('Bar', 'bar.md')
        baz = Page('Baz', 'baz.md')
        pages = [
            foo, bar, baz
        ]
        self.assertEqual(self.factory.arrange_pages(pages, PagesFile(arrange=[
            'foo.md',
            'bar.md',
            '...',
            'baz.md'
        ])), [
            foo, bar, baz
        ])

    def test_auto_arrange_index(self):
        index = Page('Index', 'index.md')
        foo = Page('Foo', 'foo.md')
        bar = Page('Bar', 'bar.md')
        pages = [
            bar, foo, index
        ]
        self.assertEqual(self.factory.arrange_pages(pages, PagesFile()), [
            index, bar, foo
        ])

    def test_auto_arrange_index_first_already(self):
        index = Page('Index', 'index.md')
        foo = Page('Foo', 'foo.md')
        bar = Page('Bar', 'bar.md')
        pages = [
            index, foo, bar
        ]
        self.assertEqual(self.factory.arrange_pages(pages, PagesFile()), [
            index, foo, bar
        ])

    def test_auto_arrange_index_file_extension(self):
        index = Page('Index', 'index.foo')
        foo = Page('Foo', 'foo.md')
        bar = Page('Bar', 'bar.md')
        pages = [
            bar, foo, index
        ]
        self.assertEqual(self.factory.arrange_pages(pages, PagesFile()), [
            index, bar, foo
        ])

    def test_auto_arrange_index_disabled(self):
        self.factory.options.disable_auto_arrange_index = True

        index = Page('Index', 'index.md')
        foo = Page('Foo', 'foo.md')
        bar = Page('Bar', 'bar.md')
        pages = [
            bar, foo, index
        ]
        self.assertEqual(self.factory.arrange_pages(pages, PagesFile()), [
            bar, foo, index
        ])

    def test_multilevel(self):
        index = Page('Foo', 'foo/index.md')
        foo = Page('Foo', 'foo/foo.md')
        bar = Page('Bar', 'foo/bar', [
            Page('BarIndex', 'foo/bar/index.md'),
            Page('BarBar', 'foo/bar/bar.md')
        ])
        pages = [
            bar, foo, index
        ]
        self.assertEqual(self.factory.arrange_pages(pages, PagesFile(arrange=[
            'index.md',
            'foo.md',
            'bar'
        ])), [
            index, foo, bar
        ])

    def test_page_not_found(self):
        pages = [
            Page('Foo', 'foo.md'),
            Page('Bar', 'bar.md')
        ]

        with self.assertRaises(PageNotFoundError):
            self.factory.arrange_pages(pages, PagesFile(arrange=[
                'index.md'
            ]))

    def test_path_none_first(self):
        none = Page('None', None)
        foo = Page('Foo', 'foo.md')
        bar = Page('Bar', 'bar.md')
        pages = [
            none, foo, bar
        ]
        self.assertEqual(self.factory.arrange_pages(pages, PagesFile(arrange=[
            'bar.md'
        ])), [
            bar, none, foo
        ])

    def test_path_none_multiple(self):
        none1 = Page('None', None)
        foo = Page('Foo', 'foo.md')
        none2 = Page('None', None)
        pages = [
            none1, foo, none2
        ]
        self.assertEqual(self.factory.arrange_pages(pages, PagesFile(arrange=[
            'foo.md'
        ])), [
            foo, none1, none2
        ])

    def test_path_none_auto_arrange_index(self):
        none1 = Page('None', None)
        index = Page('Index', 'index.md')
        none2 = Page('None', None)
        pages = [
            none1, index, none2
        ]
        self.assertEqual(self.factory.arrange_pages(pages, PagesFile()), [
            index, none1, none2
        ])

    def test_duplicate_paths_no_pages_file(self):
        foo1 = Page('Foo', 'foo.md')
        foo2 = Page('Foo', 'foo.md')
        bar = Page('Bar', 'bar.md')
        pages = [
            foo1, bar, foo2
        ]
        self.assertEqual(self.factory.arrange_pages(pages, PagesFile()), [
            foo1, bar, foo2
        ])

    def test_duplicate_paths_used_in_pages_file(self):
        foo1 = Page('Foo', 'foo.md')
        foo2 = Page('Foo', 'foo.md')
        bar = Page('Bar', 'bar.md')
        pages = [
            foo1, bar, foo2
        ]
        self.assertEqual(self.factory.arrange_pages(pages, PagesFile(arrange=[
            'foo.md'
        ])), [
            foo1, foo2, bar
        ])

    def test_duplicate_paths_auto_arrange_index(self):
        foo1 = Page('Foo', 'foo.md')
        foo2 = Page('Foo', 'foo.md')
        index = Page('Index', 'index.md')
        pages = [
            foo1, index, foo2
        ]
        self.assertEqual(self.factory.arrange_pages(pages, PagesFile()), [
            index, foo1, foo2
        ])

    def test_duplicate_arrange_entries(self):
        foo = Page('Foo', 'foo.md')
        bar = Page('Bar', 'bar.md')
        baz = Page('Baz', 'baz.md')
        pages = [
            foo, bar, baz
        ]
        self.assertEqual(self.factory.arrange_pages(pages, PagesFile(arrange=[
            'bar.md',
            'foo.md',
            'baz.md',
            'bar.md'
        ])), [
            bar, foo, baz, bar
        ])
