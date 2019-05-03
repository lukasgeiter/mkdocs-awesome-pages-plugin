from unittest import TestCase, mock

from ..meta import Meta, DuplicateRestTokenError
from .file_mock import FileMock


@mock.patch('builtins.open', new_callable=FileMock)
class TestLoadFrom(TestCase):
    def test_empty_file(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            '\n'
        )

        meta = Meta.load_from('.pages')
        self.assertEqual(meta.path, '.pages')
        self.assertIsNone(meta.title)
        self.assertEqual(meta.arrange, [])

    def test_title(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'title: Section Title\n'
        )

        meta = Meta.load_from('.pages')
        self.assertEqual(meta.path, '.pages')
        self.assertEqual(meta.title, 'Section Title')
        self.assertEqual(meta.arrange, [])

    def test_arrange(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'arrange:\n'
            '  - 2.md\n'
            '  - 1.md\n'
        )

        meta = Meta.load_from('.pages')
        self.assertEqual(meta.path, '.pages')
        self.assertIsNone(meta.title)
        self.assertEqual(meta.arrange, ['2.md', '1.md'])

    def test_title_and_arrange(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'title: Section Title\n'
            'arrange:\n'
            '  - 2.md\n'
            '  - 1.md\n'
        )

        meta = Meta.load_from('.pages')
        self.assertEqual(meta.path, '.pages')
        self.assertEqual(meta.title, 'Section Title')
        self.assertEqual(meta.arrange, ['2.md', '1.md'])

    def test_invalid_title_type(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'title:\n'
            '  - Section Title\n'
        )

        with self.assertRaises(TypeError):
            Meta.load_from('.pages')

    def test_invalid_arrange_type(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'arrange: 1.md\n'
        )

        with self.assertRaises(TypeError):
            Meta.load_from('.pages')

    def test_duplicate_rest_token(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'arrange:\n'
            '  - 2.md\n'
            '  - ...\n'
            '  - 1.md\n'
            '  - ...\n'
        )

        with self.assertRaises(DuplicateRestTokenError):
            Meta.load_from('.pages')

    def test_invalid_collapse_type(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'collapse: 1.md\n'
        )

        with self.assertRaises(TypeError):
            Meta.load_from('.pages')

    def test_invalid_collapse_single_pages_type(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'collapse_single_pages: 1.md\n'
        )

        with self.assertRaises(TypeError):
            Meta.load_from('.pages')

    def test_invalid_hide_type(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'hide: 1.md\n'
        )

        with self.assertRaises(TypeError):
            Meta.load_from('.pages')

    def test_file_not_found(self, file_mock: FileMock):
        with self.assertRaises(FileNotFoundError):
            Meta.load_from('.pages')


@mock.patch('builtins.open', new_callable=FileMock)
class TestTryLoadFrom(TestCase):
    def test(self, file_mock: FileMock):
        file_mock['.pages'].read_data = (
            'title: Section Title\n'
        )

        meta = Meta.try_load_from('.pages')
        self.assertEqual(meta.title, 'Section Title')

    def test_file_not_found(self, file_mock: FileMock):
        meta = Meta.try_load_from('.pages')
        self.assertIsInstance(meta, Meta)

    def test_none_path(self, file_mock: FileMock):
        meta = Meta.try_load_from(None)
        self.assertIsInstance(meta, Meta)
