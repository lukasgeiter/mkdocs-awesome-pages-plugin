import warnings
from pathlib import Path
from typing import List, Optional, Union

from mkdocs.structure.nav import Navigation as MkDocsNavigation, Section, Link, \
    _get_by_type, _add_parent_links, _add_previous_and_next_links
from mkdocs.structure.pages import Page

from .meta import Meta
from .options import Options
from .utils import dirname, basename, join_paths

NavigationItem = Union[Page, Section, Link]


class NavEntryNotFound(Warning):
    def __init__(self, entry: str, context: str):
        super().__init__('Nav entry "{entry}" not found. [{context}]'.format(entry=entry, context=context))


class TitleInRootHasNoEffect(Warning):
    def __init__(self, filename: str):
        super().__init__(
            'Using the "title" attribute in the {filename} file of the doc root has no effect'
            .format(filename=filename)
        )


class HideInRootHasNoEffect(Warning):
    def __init__(self, filename: str):
        super().__init__(
            'Using the "hide" attribute in the {filename} file of the doc root has no effect'
            .format(filename=filename)
        )


class AwesomeNavigation:

    def __init__(self, navigation: MkDocsNavigation, options: Options, docs_dir: str):
        self.options = options

        self.meta = NavigationMeta(navigation.items, options, docs_dir)

        if self.meta.root.title is not None:
            warnings.warn(TitleInRootHasNoEffect(self.options.filename))

        if self.meta.root.hide is not None:
            warnings.warn(HideInRootHasNoEffect(self.options.filename))

        self.items = self._process_children(
            navigation.items,
            self.options.collapse_single_pages,
            self.meta.root
        )

    def _process_children(self, children: List[NavigationItem], collapse: bool, meta: Meta) -> List[NavigationItem]:
        self._order(children, meta)
        children = self._nav(children, meta)

        result = []

        for item in children:
            if isinstance(item, Section):
                item = self._process_section(item, collapse)
                if item is None:
                    continue
            result.append(item)

        return result

    def _order(self, items: List[NavigationItem], meta: Meta):
        if meta.order is not None:
            items.sort(
                key=lambda i: basename(self._get_item_path(i)),
                reverse=meta.order == Meta.ORDER_DESC
            )

    def _nav(self, items: List[NavigationItem], meta: Meta) -> List[NavigationItem]:
        if meta.nav is None:
            return items

        items_by_basename = {basename(self._get_item_path(item)): item for item in items}

        result = []
        rest_index = None

        for index, meta_item in enumerate(meta.nav):
            if meta_item == Meta.NAV_REST_TOKEN:
                rest_index = index
            else:
                if meta_item.value in items_by_basename:
                    item = items_by_basename[meta_item.value]
                    if meta_item.title is not None:
                        item.title = meta_item.title
                    result.append(item)

                elif meta_item.title is not None:
                    result.append(Link(meta_item.title, meta_item.value))

                else:
                    warning = NavEntryNotFound(meta_item.value, meta.path)
                    if self.options.strict:
                        raise warning
                    else:
                        warnings.warn(warning)

        if rest_index is not None:
            result[rest_index:rest_index] = [item for item in items if item not in result]

        return result

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

    def to_mkdocs(self) -> MkDocsNavigation:
        pages = _get_by_type(self.items, Page)
        _add_previous_and_next_links(pages)
        _add_parent_links(self.items)
        return MkDocsNavigation(self.items, pages)


class NavigationMeta:

    def __init__(self, items: List[NavigationItem], options: Options, docs_dir: str):
        self.options = options
        self.sections = {}
        self.docs_dir = docs_dir

        root_path = self._gather_metadata(items)
        self.root = Meta.try_load_from(join_paths(root_path, self.options.filename))

    def _gather_metadata(self, items: List[NavigationItem]) -> Optional[str]:
        paths = []
        for item in items:
            if isinstance(item, Page):
                if Path(self.docs_dir) in Path(item.file.abs_src_path).parents:
                    paths.append(item.file.abs_src_path)
            elif isinstance(item, Section):
                section_dir = self._gather_metadata(item.children)
                if section_dir is not None:
                    paths.append(section_dir)
                self.sections[item] = Meta.try_load_from(join_paths(section_dir, self.options.filename))

        return self._common_dirname(paths)

    @staticmethod
    def _common_dirname(paths: List[Optional[str]]) -> Optional[str]:
        if paths:
            dirnames = [dirname(path) for path in paths]
            if len(set(dirnames)) == 1:
                return dirnames[0]
