from pathlib import Path
from unittest import TestCase, mock

from mkdocs.structure.files import File, Files

from ..meta import DuplicateRestItemError, Meta, MetaNavItem, MetaNavRestItem
from .file_mock import FileMock


@mock.patch("builtins.open", new_callable=FileMock)
class TestLoadFrom(TestCase):
    def test_empty_file(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "\n"

        meta = Meta.load_from(".pages")
        self.assertEqual(meta.path, ".pages")
        self.assertIsNone(meta.title)
        self.assertIsNone(meta.nav)

    def test_title(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "title: Section Title\n"

        meta = Meta.load_from(".pages")
        self.assertEqual(meta.path, ".pages")
        self.assertEqual(meta.title, "Section Title")
        self.assertIsNone(meta.nav)

    def test_arrange(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "arrange:\n" "  - 2.md\n" "  - 1.md\n"

        meta = Meta.load_from(".pages")
        self.assertEqual(meta.path, ".pages")
        self.assertIsNone(meta.title)
        self.assertEqual(meta.nav, [MetaNavItem("2.md"), MetaNavItem("1.md"), MetaNavRestItem("...")])

    def test_arrange_rest_token(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "arrange:\n" "  - 2.md\n" "  - ...\n" "  - 1.md\n"

        meta = Meta.load_from(".pages")
        self.assertEqual(meta.path, ".pages")
        self.assertIsNone(meta.title)
        self.assertEqual(meta.nav, [MetaNavItem("2.md"), MetaNavRestItem("..."), MetaNavItem("1.md")])

    def test_title_and_arrange(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "title: Section Title\n" "arrange:\n" "  - 2.md\n" "  - 1.md\n"

        meta = Meta.load_from(".pages")
        self.assertEqual(meta.path, ".pages")
        self.assertEqual(meta.title, "Section Title")
        self.assertEqual(meta.nav, [MetaNavItem("2.md"), MetaNavItem("1.md"), MetaNavRestItem("...")])

    def test_arrange_and_nav(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "arrange:\n" "  - 2.md\n" "  - 1.md\n" "nav:\n" "  - 1.md\n" "  - 2.md\n"

        meta = Meta.load_from(".pages")
        self.assertEqual(meta.path, ".pages")
        self.assertIsNone(meta.title)
        self.assertEqual(meta.nav, [MetaNavItem("1.md"), MetaNavItem("2.md")])

    def test_nav_list(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "nav:\n" "  - 2.md\n" "  - 1.md\n"

        meta = Meta.load_from(".pages")
        self.assertEqual(meta.nav, [MetaNavItem("2.md"), MetaNavItem("1.md")])

    def test_nav_titles(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "nav:\n" "  - Two: 2.md\n" "  - One: 1.md\n"

        meta = Meta.load_from(".pages")
        self.assertEqual(meta.nav, [MetaNavItem("2.md", "Two"), MetaNavItem("1.md", "One")])

    def test_nav_mixed(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "nav:\n" "  - 2.md\n" "  - One: 1.md\n"

        meta = Meta.load_from(".pages")
        self.assertEqual(meta.nav, [MetaNavItem("2.md"), MetaNavItem("1.md", "One")])

    def test_nav_rest(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "nav:\n" "  - 2.md\n" "  - ...\n" "  - One: 1.md\n"

        meta = Meta.load_from(".pages")
        self.assertEqual(
            meta.nav,
            [MetaNavItem("2.md"), MetaNavRestItem("..."), MetaNavItem("1.md", "One")],
        )

    def test_order_none(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "\n"

        meta = Meta.load_from(".pages")
        self.assertIsNone(meta.order)

    def test_order_asc(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "order: asc\n"

        meta = Meta.load_from(".pages")
        self.assertEqual(meta.order, Meta.ORDER_ASC)

    def test_order_desc(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "order: desc\n"

        meta = Meta.load_from(".pages")
        self.assertEqual(meta.order, Meta.ORDER_DESC)

    def test_invalid_title_type(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "title:\n" "  - Section Title\n"

        with self.assertRaises(TypeError):
            Meta.load_from(".pages")

    def test_invalid_arrange_type(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "arrange: 1.md\n"

        with self.assertRaises(TypeError):
            Meta.load_from(".pages")

    def test_duplicate_rest_token(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "arrange:\n" "  - 2.md\n" "  - ...\n" "  - 1.md\n" "  - ...\n"

        with self.assertRaises(DuplicateRestItemError):
            Meta.load_from(".pages")

    def test_invalid_collapse_type(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "collapse: 1.md\n"

        with self.assertRaises(TypeError):
            Meta.load_from(".pages")

    def test_invalid_collapse_single_pages_type(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "collapse_single_pages: 1.md\n"

        with self.assertRaises(TypeError):
            Meta.load_from(".pages")

    def test_invalid_hide_type(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "hide: 1.md\n"

        with self.assertRaises(TypeError):
            Meta.load_from(".pages")

    def test_invalid_order(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "order: foo\n"

        with self.assertRaises(TypeError):
            Meta.load_from(".pages")

    def test_invalid_nav_type(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "nav: 1.md\n"

        with self.assertRaises(TypeError):
            Meta.load_from(".pages")

    def test_invalid_nav_item_boolean(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "nav:\n" "  - off\n"

        with self.assertRaises(TypeError):
            Meta.load_from(".pages")

    def test_invalid_nav_item_title_boolean(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "nav:\n" "  - off: foo\n"

        with self.assertRaises(TypeError):
            Meta.load_from(".pages")

    def test_invalid_nav_item_value_boolean(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "nav:\n" "  - foo: off\n"

        with self.assertRaises(TypeError):
            Meta.load_from(".pages")

    def test_invalid_nav_item_dict_too_many_entries(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "nav:\n" "  - foo: foo\n" "    bar: bar\n"

        with self.assertRaises(TypeError):
            Meta.load_from(".pages")

    def test_duplicate_nav_rest_token(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "nav:\n" "  - 2.md\n" "  - ...\n" "  - 1.md\n" "  - ...\n"

        with self.assertRaises(DuplicateRestItemError):
            Meta.load_from(".pages")

    def test_duplicate_nav_rest_pattern_glob(self, file_mock: FileMock):
        file_mock[".pages"].read_data = "nav:\n" "  - ... | a*.md\n" "  - 1.md\n" "  - ... | a*.md\n"

        with self.assertRaises(DuplicateRestItemError):
            Meta.load_from(".pages")

    def test_file_not_found(self, file_mock: FileMock):
        with self.assertRaises(FileNotFoundError):
            Meta.load_from(".pages")


@mock.patch("builtins.open", new_callable=FileMock)
class TestTryLoadFrom(TestCase):
    def test_in_docs_dir(self, file_mock: FileMock):
        docs_path = Path("docs").resolve()
        file_mock[str(docs_path / ".pages")].read_data = "title: Section Title\n"
        files = Files([File(".pages", str(docs_path), "", False)])

        meta = Meta.try_load_from_files(".pages", files)
        self.assertEqual(meta.title, "Section Title")
        self.assertEqual(meta.path, ".pages")

    def test_file_not_found(self, file_mock: FileMock):
        meta = Meta.try_load_from_files(".pages", Files([]))
        self.assertIsInstance(meta, Meta)

    def test_none_path(self, file_mock: FileMock):
        meta = Meta.try_load_from_files(None, Files([]))
        self.assertIsInstance(meta, Meta)
