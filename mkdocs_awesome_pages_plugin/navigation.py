import warnings
from typing import List, Optional, Union, Dict

from mkdocs.structure.nav import Navigation as MkDocsNavigation, Section, Link, \
    _get_by_type, _add_parent_links, _add_previous_and_next_links
from mkdocs.structure.pages import Page

from .arrange import arrange, InvalidArrangeEntry
from .meta import Meta
from .options import Options
from .utils import dirname, basename, join_paths

import io
from mkdocs.utils import meta as mkdocs_meta

NavigationItem = Union[Page, Section, Link]


class ArrangeEntryNotFound(Exception):
    def __init__(self, entry: str, context: str):
        super().__init__('Arrange entry "{entry}" not found. [{context}]'.format(entry=entry, context=context))


class TitleInRootWarning(Warning):
    pass


class HideInRootWarning(Warning):
    pass


class AwesomeNavigation:

    def __init__(self, navigation: MkDocsNavigation, options: Options):
        self.options = options
        self.Allpages = []
        self.maximum_file_homepage = int(float(options.maximum_file_homepage))
        self.maximum_days_ahead = int(float(options.maximum_days_ahead))
        self.meta = NavigationMeta(navigation.items, options)

        if self.meta.root.title is not None:
            warnings.warn('Using the "title" attribute in the {filename} file of the doc root has no effect'
                          .format(filename=self.options.filename), category=TitleInRootWarning)

        if self.meta.root.hide is not None:
            warnings.warn('Using the "hide" attribute in the {filename} file of the doc root has no effect'
                          .format(filename=self.options.filename), category=HideInRootWarning)

        self.items = self._process_children(
            navigation.items,
            self.options.collapse_single_pages,
            self.meta.root
        )

    def _process_children(self, children: List[NavigationItem], collapse: bool, meta: Meta) -> List[NavigationItem]:
        children = self._arrange_items(children, meta)
        result = []

        for item in children:
            if isinstance(item, Section):
                item = self._process_section(item, collapse)
                if item is None:
                    continue
            result.append(item)

        return result

    def _arrange_items(self, items: List[NavigationItem], meta: Meta) -> List[NavigationItem]:
        if meta.arrange is not None:
            try:
                return arrange(items, meta.arrange, lambda item: basename(self._get_item_path(item)))
            except InvalidArrangeEntry as e:
                raise ArrangeEntryNotFound(e.value, meta.path)
        return items

    def _process_section(self, section: Section, collapse_recursive: bool) -> Optional[NavigationItem]:
        meta = self.meta.sections[section]

        if meta.hide is True:
            return None

        if meta.collapse_single_pages is not None:
            collapse_recursive = meta.collapse_single_pages

        self._set_title(section, meta)

        section.children = self._process_children(section.children, collapse_recursive, meta)

        if not section.children:
            return None

        return self._collapse(section, meta.collapse, collapse_recursive)

    def _get_item_path(self, item: NavigationItem) -> Optional[str]:
        if isinstance(item, Section):
            return dirname(self.meta.sections[item].path)
        elif isinstance(item, Page):
            return item.file.abs_src_path

    @staticmethod
    def _set_title(section: Section, meta: Meta):
        if meta.title is not None:
            section.title = meta.title

    @staticmethod
    def _collapse(section: Section, collapse: Optional[bool], collapse_recursive: bool) -> NavigationItem:
        if collapse is None:
            collapse = collapse_recursive

        if collapse and len(section.children) == 1:
            return section.children[0]
        return section

    def _get_meta(self, page_):
        with io.open(page_.file.abs_src_path, 'r', encoding='utf-8-sig', errors='strict') as f:
            source = f.read()
        
        _, page_.meta = mkdocs_meta.get_data(source)

    def to_mkdocs(self) -> MkDocsNavigation:
        pages = _get_by_type(self.items, Page)
        _add_previous_and_next_links(pages)
        _add_parent_links(self.items)

        from datetime import datetime

        date_time = datetime.today()
        diff_day_list = []
        page_list = []
        for page in pages:
            self._get_meta(page)
            if 'time' in page.meta:
                page_time = page.meta['time']
                print(page_time)
                year = int(page_time[0:4])
                month = int(page_time[4:6])
                day = int(page_time[6:8])
                page_datetime = datetime(year, month, day)
                time_delta = date_time - page_datetime
                total_seconds = time_delta.total_seconds()
                total_days = total_seconds / 3600 / 24
            else:
                total_days = 999999
            diff_day_list.append(total_days)
        
        import numpy as np
        argsorted = np.argsort(diff_day_list)
        for index in argsorted:
            if pages[index].is_homepage:
                page_list.insert(0, pages[index])
            else:
                page_list.append(pages[index])
            if diff_day_list[index] < self.maximum_days_ahead:
                if len(page_list) <= self.maximum_file_homepage:
                    pages[index].shown_in_homepage = True
                    continue
            pages[index].shown_in_homepage = False
        # _add_previous_and_next_links(page_list)
        print('Finishing daytime processing')
        return MkDocsNavigation(self.items, page_list)


class NavigationMeta:

    def __init__(self, items: List[NavigationItem], options: Options):
        self.options = options
        self.sections = {}

        root_path = self._gather_metadata(items)
        self.root = Meta.try_load_from(join_paths(root_path, self.options.filename))

    def _gather_metadata(self, items: List[NavigationItem]) -> Optional[str]:
        paths = []
        for item in items:
            if isinstance(item, Page):
                paths.append(item.file.abs_src_path)
            elif isinstance(item, Section):
                section_dir = self._gather_metadata(item.children)
                paths.append(section_dir)
                self.sections[item] = Meta.try_load_from(join_paths(section_dir, self.options.filename))

        return self._common_dirname(paths)

    @staticmethod
    def _common_dirname(paths: List[Optional[str]]) -> Optional[str]:
        if paths:
            dirnames = [dirname(path) for path in paths]
            if len(set(dirnames)) == 1:
                return dirnames[0]
