import warnings
from typing import List, Optional, Union, Dict

from mkdocs.structure.nav import Navigation as MkDocsNavigation, Section, Link, \
    _get_by_type, _add_parent_links, _add_previous_and_next_links
from mkdocs.structure.pages import Page

from .arrange import arrange, InvalidArrangeEntry
from .meta import Meta
from .options import Options
from .utils import dirname, basename, join_paths

NavigationItem = Union[Page, Section, Link]


class ArrangeEntryNotFound(Exception):
    def __init__(self, entry: str, context: str):
        super().__init__('Arrange entry "{entry}" not found. [{context}]'.format(entry=entry, context=context))


class TitleInRootWarning(Warning):
    pass


class AwesomeNavigation:

    def __init__(self, navigation: MkDocsNavigation, options: Options):
        self.options = options

        self.meta = NavigationMeta(navigation.items, options)

        if self.meta.root.title is not None:
            warnings.warn('Using the "title" attribute in the {filename} file of the doc root has no effect'
                          .format(filename=self.options.filename), category=TitleInRootWarning)

        self.items = self._process_children(
            navigation.items,
            self.options.collapse_single_pages,
            self.meta.root
        )

    def _process_children(self, children: List[NavigationItem], collapse: bool, meta: Meta) -> List[NavigationItem]:
        children = self._arrange_items(children, meta)

        for index, item in enumerate(children):
            if isinstance(item, Section):
                children[index] = self._process_section(item, collapse)

        return children

    def _arrange_items(self, items: List[NavigationItem], meta: Meta) -> List[NavigationItem]:
        if meta.arrange is not None:
            try:
                return arrange(items, meta.arrange, lambda item: basename(self._get_item_path(item)))
            except InvalidArrangeEntry as e:
                raise ArrangeEntryNotFound(e.value, meta.path)
        return items

    def _process_section(self, section: Section, collapse_recursive: bool) -> NavigationItem:
        meta = self.meta.sections[section]

        if meta.collapse_single_pages is not None:
            collapse_recursive = meta.collapse_single_pages

        self._set_title(section, meta)

        section.children = self._process_children(section.children, collapse_recursive, meta)

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

    def to_mkdocs(self) -> MkDocsNavigation:
        pages = _get_by_type(self.items, Page)
        _add_previous_and_next_links(pages)
        _add_parent_links(self.items)
        return MkDocsNavigation(self.items, pages)


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
