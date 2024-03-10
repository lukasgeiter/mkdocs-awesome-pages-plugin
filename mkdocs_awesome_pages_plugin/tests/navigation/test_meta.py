import os.path
from typing import List, Optional, Set
from unittest import TestCase

from mkdocs.structure.files import File, Files
from mkdocs.structure.nav import Section
from mkdocs.structure.pages import Page

from ...meta import Meta, MetaNavRestItem, RestType
from ...navigation import NavigationItem, NavigationMeta
from ...options import Options
from ...utils import normpath
from .base import NavigationTestCase


class TestCommonDirname(TestCase):
    def test_all_match(self):
        self.assertEqual(NavigationMeta._common_dirname(["a/1.md", "a/2.md"]), "a")

    def test_some_match(self):
        self.assertEqual(NavigationMeta._common_dirname(["a/1.md", "a/2.md", "b/3.md"]), None)

    def test_none_match(self):
        self.assertEqual(NavigationMeta._common_dirname(["a/1.md", "b/2.md"]), None)

    def test_empty(self):
        self.assertEqual(NavigationMeta._common_dirname([]), None)

    def test_some_none_entries(self):
        self.assertEqual(NavigationMeta._common_dirname(["section/page.md", None]), None)

    def test_all_none_entries(self):
        self.assertEqual(NavigationMeta._common_dirname([None, None]), None)


class TestMeta(NavigationTestCase):
    def assertMeta(self, actual: Meta, expected: Optional[Meta] = None, *, path: Optional[str] = None):
        if expected is None:
            expected = Meta(path=path)

        self.assertEqual(actual.collapse_single_pages, expected.collapse_single_pages)
        self.assertEqual(actual.collapse, expected.collapse)
        self.assertEqual(actual.title, expected.title)
        self.assertEqual(normpath(actual.path), normpath(expected.path))

    def assertEmptyMeta(self, meta: Meta):
        self.assertMeta(meta)

    def setUp(self):
        super(TestMeta, self).setUp()
        self.options = Options(filename=".pages", collapse_single_pages=False, strict=True)

    def _make_nav_meta(
        self,
        items: List[NavigationItem],
        options: Options,
        explicit_sections: Set[Section] = frozenset(),
    ):
        files = Files([])
        config_dirs = set()

        def populate_config_dirs(items: List[NavigationItem]):
            for item in items:
                if isinstance(item, Page):
                    config_dirs.add(
                        (
                            os.path.dirname(item.file.src_path),
                            item.file.abs_src_path[: -len(item.file.src_path)],
                        )
                    )
                    files.append(item.file)
                elif isinstance(item, Section):
                    populate_config_dirs(item.children)

        populate_config_dirs(items)

        for rel_config_dir, abs_docs_dir in config_dirs:
            files.append(
                File(
                    os.path.join(rel_config_dir, options.filename),
                    src_dir=abs_docs_dir,
                    dest_dir="",
                    use_directory_urls=False,
                )
            )

        return NavigationMeta(items, options, files, explicit_sections)

    def test_empty(self):
        meta = self._make_nav_meta([], self.options)

        self.assertEqual(len(meta.sections), 0)
        self.assertEmptyMeta(meta.root)

    def test_page_in_root(self):
        meta = self._make_nav_meta(
            [self.page("Page", "page.md")],
            self.options,
        )

        self.assertEqual(len(meta.sections), 0)
        self.assertMeta(meta.root, path=".pages")

    def test_empty_section(self):
        section = self.section("Section", [])
        meta = self._make_nav_meta([section], self.options)

        self.assertEqual(len(meta.sections), 1)
        self.assertEmptyMeta(meta.sections[section])
        self.assertEmptyMeta(meta.root)

    def test_section(self):
        section = self.section("Section", [self.page("Page", "section/page.md")])
        meta = self._make_nav_meta([section], self.options)

        self.assertEqual(len(meta.sections), 1)
        self.assertMeta(meta.sections[section], path="section/.pages")
        self.assertMeta(meta.root, path=".pages")

    def test_multiple_sections(self):
        b = self.section("B", [self.page("1", "a/b/1.md")])
        a = self.section("A", [b])

        d = self.section("D", [])
        e = self.section("E", [self.page("2", "c/e/2.md")])
        c = self.section("C", [d, e])

        meta = self._make_nav_meta([a, c], self.options)

        self.assertEqual(len(meta.sections), 5)

        self.assertMeta(meta.sections[a], path="a/.pages")
        self.assertMeta(meta.sections[b], path="a/b/.pages")

        self.assertMeta(meta.sections[c], path="c/.pages")
        self.assertEmptyMeta(meta.sections[d])
        self.assertMeta(meta.sections[e], path="c/e/.pages")

        self.assertMeta(meta.root, path=".pages")

    def test_filename_option(self):
        section = self.section("Section", [self.page("Page", "section/page.md")])
        meta = self._make_nav_meta([section], Options(filename=".index", collapse_single_pages=False, strict=True))

        self.assertEqual(len(meta.sections), 1)
        self.assertMeta(meta.sections[section], path="section/.index")
        self.assertMeta(meta.root, path=".index")

    def test_links(self):
        meta = self._make_nav_meta([self.page("Page", "page.md"), self.link("Link")], self.options)

        self.assertEqual(len(meta.sections), 0)
        self.assertMeta(meta.root, path=".pages")

    def test_no_common_dirname(self):
        section = self.section("Section", [self.page("1", "a/1.md"), self.page("2", "b/2.md")])
        meta = self._make_nav_meta([section], self.options)

        self.assertEqual(len(meta.sections), 1)
        self.assertEmptyMeta(meta.sections[section])
        self.assertEmptyMeta(meta.root)


class TestRestParsing(NavigationTestCase):
    def test_all(self):
        item = MetaNavRestItem("...")

        self.assertIsNone(item.pattern)
        self.assertEqual(item.type, RestType.ALL)
        self.assertFalse(item.flat)

    def test_all_flat(self):
        item = MetaNavRestItem("...|flat")

        self.assertIsNone(item.pattern)
        self.assertEqual(item.type, RestType.ALL)
        self.assertTrue(item.flat)

    def test_all_flat_spaces(self):
        item = MetaNavRestItem("... | flat")

        self.assertIsNone(item.pattern)
        self.assertEqual(item.type, RestType.ALL)
        self.assertTrue(item.flat)

    def test_glob_implicit(self):
        item = MetaNavRestItem("...|foo")

        self.assertEqual(item.pattern, "foo")
        self.assertEqual(item.type, RestType.GLOB)
        self.assertFalse(item.flat)

    def test_glob_implicit_spaces(self):
        item = MetaNavRestItem("... | foo")

        self.assertEqual(item.pattern, "foo")
        self.assertEqual(item.type, RestType.GLOB)
        self.assertFalse(item.flat)

    def test_glob_implicit_trailing_space(self):
        item = MetaNavRestItem("... | foo ")

        self.assertEqual(item.pattern, "foo ")
        self.assertEqual(item.type, RestType.GLOB)
        self.assertFalse(item.flat)

    def test_glob_implicit_flat(self):
        item = MetaNavRestItem("...|flat|foo")

        self.assertEqual(item.pattern, "foo")
        self.assertEqual(item.type, RestType.GLOB)
        self.assertTrue(item.flat)

    def test_glob_implicit_flat_spaces(self):
        item = MetaNavRestItem("... | flat | foo")

        self.assertEqual(item.pattern, "foo")
        self.assertEqual(item.type, RestType.GLOB)
        self.assertTrue(item.flat)

    def test_glob_implicit_flat_trailing_space(self):
        item = MetaNavRestItem("... | flat | foo ")

        self.assertEqual(item.pattern, "foo ")
        self.assertEqual(item.type, RestType.GLOB)
        self.assertTrue(item.flat)

    def test_glob_explicit(self):
        item = MetaNavRestItem("...|glob=foo")

        self.assertEqual(item.pattern, "foo")
        self.assertEqual(item.type, RestType.GLOB)
        self.assertFalse(item.flat)

    def test_glob_explicit_spaces(self):
        item = MetaNavRestItem("... | glob=foo")

        self.assertEqual(item.pattern, "foo")
        self.assertEqual(item.type, RestType.GLOB)
        self.assertFalse(item.flat)

    def test_glob_explicit_trailing_space(self):
        item = MetaNavRestItem("... | glob=foo ")

        self.assertEqual(item.pattern, "foo ")
        self.assertEqual(item.type, RestType.GLOB)
        self.assertFalse(item.flat)

    def test_glob_explicit_leading_space(self):
        item = MetaNavRestItem("... | glob= foo")

        self.assertEqual(item.pattern, " foo")
        self.assertEqual(item.type, RestType.GLOB)
        self.assertFalse(item.flat)

    def test_glob_explicit_flat(self):
        item = MetaNavRestItem("...|flat|glob=foo")

        self.assertEqual(item.pattern, "foo")
        self.assertEqual(item.type, RestType.GLOB)
        self.assertTrue(item.flat)

    def test_glob_explicit_flat_spaces(self):
        item = MetaNavRestItem("... | flat | glob=foo")

        self.assertEqual(item.pattern, "foo")
        self.assertEqual(item.type, RestType.GLOB)
        self.assertTrue(item.flat)

    def test_glob_explicit_flat_trailing_space(self):
        item = MetaNavRestItem("... | flat | glob=foo ")

        self.assertEqual(item.pattern, "foo ")
        self.assertEqual(item.type, RestType.GLOB)
        self.assertTrue(item.flat)

    def test_glob_explicit_flat_leading_space(self):
        item = MetaNavRestItem("... | flat | glob= foo")

        self.assertEqual(item.pattern, " foo")
        self.assertEqual(item.type, RestType.GLOB)
        self.assertTrue(item.flat)

    def test_regex(self):
        item = MetaNavRestItem("...|regex=foo")

        self.assertEqual(item.pattern, "foo")
        self.assertEqual(item.type, RestType.REGEX)
        self.assertFalse(item.flat)

    def test_regex_spaces(self):
        item = MetaNavRestItem("... | regex=foo")

        self.assertEqual(item.pattern, "foo")
        self.assertEqual(item.type, RestType.REGEX)
        self.assertFalse(item.flat)

    def test_regex_trailing_space(self):
        item = MetaNavRestItem("... | regex=foo ")

        self.assertEqual(item.pattern, "foo ")
        self.assertEqual(item.type, RestType.REGEX)
        self.assertFalse(item.flat)

    def test_regex_leading_space(self):
        item = MetaNavRestItem("... | regex= foo")

        self.assertEqual(item.pattern, " foo")
        self.assertEqual(item.type, RestType.REGEX)
        self.assertFalse(item.flat)

    def test_regex_flat(self):
        item = MetaNavRestItem("...|flat|regex=foo")

        self.assertEqual(item.pattern, "foo")
        self.assertEqual(item.type, RestType.REGEX)
        self.assertTrue(item.flat)

    def test_regex_flat_spaces(self):
        item = MetaNavRestItem("... | flat | regex=foo")

        self.assertEqual(item.pattern, "foo")
        self.assertEqual(item.type, RestType.REGEX)
        self.assertTrue(item.flat)

    def test_regex_flat_trailing_space(self):
        item = MetaNavRestItem("... | flat | regex=foo ")

        self.assertEqual(item.pattern, "foo ")
        self.assertEqual(item.type, RestType.REGEX)
        self.assertTrue(item.flat)

    def test_regex_flat_leading_space(self):
        item = MetaNavRestItem("... | flat | regex= foo")

        self.assertEqual(item.pattern, " foo")
        self.assertEqual(item.type, RestType.REGEX)
        self.assertTrue(item.flat)
