import os
import warnings
from functools import reduce
from typing import List, Union, Optional, Dict

from . import markdown
from .page import Page, RootPage
from .pagesfile import PagesFile
from .options import Options


class PageNotFoundError(Exception):
    def __init__(self, page: str, context: str = None):
        message = 'Page "{page}" not found.'
        if context:
            message += ' [{context}]'

        super().__init__(message.format(page=page, context=context))


class TitleInRootPagesFileWarning(Warning):
    pass


class Factory:

    INDEX_PAGE_NAME = 'index'

    def __init__(self, options: Options):
        self.options = options

    def create(self, config: List) -> RootPage:
        """ Creates a root page containing the whole tree of pages from the mkdocs config """
        children = self._create_pages(config)

        pages_file = self._load_pages_file('')
        if pages_file.title is not None:
            warnings.warn(
                'Using the "title" attribute in the {filename} file of the doc root has no effect'
                    .format(filename=self.options.filename),
                TitleInRootPagesFileWarning)

        children = self.arrange_pages(children, pages_file)
        collapse_single_pages = (pages_file.collapse_single_pages if pages_file.collapse_single_pages is not None
                                 else self.options.collapse_single_pages)

        return RootPage(children, collapse_single_pages)

    def create_page(self, config_entry: Union[Dict, str]) -> Page:
        """ Creates a page from an entry in the mkdocs config """
        if isinstance(config_entry, str):
            return self._create_leaf_page(None, config_entry)

        # The config dictionary always contains one entry, retrieve it
        [title, value] = next(iter(config_entry.items()))

        if isinstance(value, str):
            return self._create_leaf_page(title, value)
        else:
            return self._create_branch_page(title, value)

    def _create_pages(self, config: List) -> List[Page]:
        """ Calls create_page for every entry in the config list """
        return [self.create_page(c) for c in config]

    def _create_leaf_page(self, title: Optional[str], path: str) -> Page:
        """ Creates a leaf page, a page pointing to an actual markdown file """
        try:
            with open(path, encoding='utf-8') as file:
                title = markdown.extract_h1(file)
        except FileNotFoundError:
            pass

        return Page(title, path)

    def _create_branch_page(self, title: str, config_children: list) -> Page:
        """ Creates a branch page, a directory page with child pages """
        children = self._create_pages(config_children)
        path = self.common_dirname(children)

        pages_file = self._load_pages_file(path)
        title = pages_file.title or title

        children = self.arrange_pages(children, pages_file)

        return Page(title, path, children,
                    collapse_single_pages=pages_file.collapse_single_pages, collapse=pages_file.collapse)

    def _load_pages_file(self, path: str):
        """ Loads and parses the pages file for a given path """
        try:
            if path is None:
                raise FileNotFoundError
            return PagesFile.load_from(os.path.join(path, self.options.filename))
        except FileNotFoundError:
            # Default to empty pages file
            return PagesFile()

    def common_dirname(self, children: List[Page]) -> Optional[str]:
        """ Determines the common dirname of all given pages """
        if children:
            return reduce(self._common_dirname, children, children[0].dirname)

    def _common_dirname(self, path: Optional[str], page: Page) -> Optional[str]:
        """ Reduces pages to a common dirname """
        if page and path is not None and page.dirname == path:
            return path

    def arrange_pages(self, pages: List[Page], pages_file: PagesFile) -> List[Page]:
        """ Sorts the given pages based on the arrange configuration from the pages file """
        pages_by_basename = self._group_pages_by_basename(pages)
        arranged_pages = set()
        rest_index = None
        result = []

        # Add pages from arrange configuration
        for index, path in enumerate(pages_file.arrange):
            if path == PagesFile.ARRANGE_REST_TOKEN:
                rest_index = index
            elif path in pages_by_basename:
                matching_pages = pages_by_basename[path]
                arranged_pages.update(matching_pages)
                result.extend(matching_pages)
            else:
                raise PageNotFoundError(path, pages_file.path)

        if rest_index is None:
            # If no rest token is used in the arrange configuration, add remaining pages at the end
            rest_index = len(result)

        # Add remaining pages
        for page in pages:
            if page in arranged_pages:
                # Skip pages that have already been added
                continue

            if (
                not pages_file.arrange
                and not self.options.disable_auto_arrange_index
                and page.basename is not None
                and os.path.splitext(page.basename)[0] == self.INDEX_PAGE_NAME
            ):
                # Automatically position index file at the beginning
                result.insert(0, page)
            else:
                result.insert(rest_index, page)

            rest_index += 1

        return result

    def _group_pages_by_basename(self, pages: List[Page]) -> Dict[str, List[Page]]:
        """ Creates a dictionary with mapping basenames to a list of matching pages """
        result = {}
        for page in pages:
            if page.basename in result:
                result[page.basename].append(page)
            else:
                result[page.basename] = [page]
        return result
