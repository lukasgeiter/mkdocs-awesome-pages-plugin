from unittest import TestCase, mock

from ..pagesfile import PagesFile, DuplicateRestTokenError
from .file_mock import FileMock


@mock.patch('builtins.open', new_callable=FileMock)
class TestPagesFile(TestCase):
    def test_empty_file(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            '\n'
        )

        pages_file = PagesFile.load_from('.pages')
        self.assertEqual(pages_file.path, '.pages')
        self.assertIsNone(pages_file.title)
        self.assertEqual(pages_file.arrange, [])

    def test_title(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'title: Foo\n'
        )

        pages_file = PagesFile.load_from('.pages')
        self.assertEqual(pages_file.path, '.pages')
        self.assertEqual(pages_file.title, 'Foo')
        self.assertEqual(pages_file.arrange, [])

    def test_arrange(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'arrange:\n'
            '  - foo.md\n'
            '  - bar.md\n'
        )

        pages_file = PagesFile.load_from('.pages')
        self.assertEqual(pages_file.path, '.pages')
        self.assertIsNone(pages_file.title)
        self.assertEqual(pages_file.arrange, ['foo.md', 'bar.md'])

    def test_title_and_arrange(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'title: Foo\n'
            'arrange:\n'
            '  - foo.md\n'
            '  - bar.md\n'
        )

        pages_file = PagesFile.load_from('.pages')
        self.assertEqual(pages_file.path, '.pages')
        self.assertEqual(pages_file.title, 'Foo')
        self.assertEqual(pages_file.arrange, ['foo.md', 'bar.md'])

    def test_invalid_title_type(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'title:\n'
            '  - Foo\n'
        )

        with self.assertRaises(TypeError):
            PagesFile.load_from('.pages')

    def test_invalid_arrange_type(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'arrange: Foo\n'
        )

        with self.assertRaises(TypeError):
            PagesFile.load_from('.pages')

    def test_duplicate_rest_token(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'arrange:\n'
            '  - foo.md\n'
            '  - ...\n'
            '  - bar.md\n'
            '  - ...\n'
        )

        with self.assertRaises(DuplicateRestTokenError):
            PagesFile.load_from('.pages')

    def test_invalid_collapse_type(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'collapse: foo\n'
        )

        with self.assertRaises(TypeError):
            PagesFile.load_from('.pages')

    def test_invalid_collapse_single_pages_type(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'collapse_single_pages: foo\n'
        )

        with self.assertRaises(TypeError):
            PagesFile.load_from('.pages')
