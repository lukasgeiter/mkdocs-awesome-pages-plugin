import os.path
from typing import List, Optional, Union
from unittest import TestCase, mock

from mkdocs.structure.files import File, Files
from mkdocs.structure.nav import Link
from mkdocs.structure.nav import Navigation as MkDocsNavigation
from mkdocs.structure.nav import Section
from mkdocs.structure.pages import Page

from ...meta import Meta
from ...navigation import AwesomeNavigation, NavigationItem, get_by_type
from ...options import Options


class NavigationMetaMock:
    def __init__(self):
        self.sections = {}
        self.root = Meta()


class NavigationTestCase(TestCase):
    @staticmethod
    def page(title: str, path: Optional[str] = None) -> Page:
        return Page(title, File(path or title + ".md", os.path.abspath("docs"), "", False), {})

    @staticmethod
    def link(title: str, url: Optional[str] = None):
        if url is None:
            url = title
        return Link(title, url)

    def section(
        self,
        title: str,
        items: List[Union[NavigationItem, Meta]],
        path: Optional[str] = None,
    ) -> Section:
        children = []
        if path is not None:
            path = os.path.join(path, ".pages")
        meta = Meta(path=path)
        for item in items:
            if isinstance(item, Meta):
                meta = item
            else:
                children.append(item)

        section = Section(title, children)
        self.meta_mock.sections[section] = meta
        return section

    def createAwesomeNavigation(
        self, items: List[NavigationItem], *, collapse_single_pages: bool = False, strict: bool = True
    ) -> AwesomeNavigation:
        children = []
        meta = None
        for item in items:
            if isinstance(item, Meta):
                meta = item
            else:
                children.append(item)

        if meta is not None:
            self.meta_mock.root = meta

        return AwesomeNavigation(
            children,
            Options(
                filename=".pages",
                collapse_single_pages=collapse_single_pages,
                strict=strict,
            ),
            files=Files([]),
            explicit_sections=set(),
        )

    def assertNavigationEqual(self, actual: List[NavigationItem], expected: List[NavigationItem]):
        self.assertEqual(len(actual), len(expected))
        for i, actual_item in enumerate(actual):
            expected_item = expected[i]
            self.assertEqual(actual_item.title, expected_item.title)

            if isinstance(expected_item, Section):
                self.assertIsInstance(actual_item, Section)
                self.assertNavigationEqual(actual_item.children, expected_item.children)
            elif isinstance(expected_item, Page):
                self.assertIsInstance(actual_item, Page)
                self.assertEqual(actual_item.file.src_path, expected_item.file.src_path)
            else:
                self.assertIsInstance(actual_item, Link)
                self.assertEqual(actual_item.url, expected_item.url)

    def assertValidNavigation(
        self, navigation: MkDocsNavigation, *, assert_previous_next: bool = True, assert_parent: bool = True
    ):
        pages = get_by_type(navigation, Page)

        if assert_previous_next:
            bookended = [None] + pages + [None]
            zipped = zip(bookended[:-2], bookended[1:-1], bookended[2:])
            for page0, page1, page2 in zipped:
                self.assertEqual(
                    page1.previous_page,
                    page0,
                    "Incorrect previous_page reference in {}".format(page1),
                )
                self.assertEqual(
                    page1.next_page,
                    page2,
                    "Incorrect next_page reference in {}".format(page1),
                )

        if assert_parent:
            sections = get_by_type(navigation, Section)

            for section in sections:
                for child in section.children:
                    self.assertEqual(
                        child.parent,
                        section,
                        "Incorrect parent reference in {}".format(child),
                    )

        self.assertEqual(navigation.pages, pages)

    def setUp(self):
        patcher = mock.patch("mkdocs_awesome_pages_plugin.navigation.NavigationMeta")
        self.addCleanup(patcher.stop)
        m = patcher.start()
        m.return_value = self.meta_mock = NavigationMetaMock()
