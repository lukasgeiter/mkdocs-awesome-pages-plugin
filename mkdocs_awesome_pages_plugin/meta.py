import collections.abc
import re
from enum import Enum
from pathlib import PurePath
from typing import Any, Iterator, List, Optional, Union

import yaml
from mkdocs.structure.files import Files
from wcmatch import glob


class DuplicateRestItemError(Exception):
    def __init__(self, item: str, context: str):
        super().__init__('Duplicate rest entry "{item}" [{context}]'.format(context=context, item=item))


class MetaNavItem:
    def __init__(self, value: Union[str, List["MetaNavItem"]], title: Optional[str] = None):
        self.value = value
        self.title = title

    def __eq__(self, other: object) -> bool:
        return isinstance(other, MetaNavItem) and self.value == other.value and self.title == other.title

    def __hash__(self):
        return hash((self.value, self.title))

    @staticmethod
    def from_yaml(item: Union[str, dict], context: str):
        if MetaNavRestItem.is_rest(item):
            return MetaNavRestItem(item)

        if isinstance(item, str):
            return MetaNavItem(item)

        if isinstance(item, dict) and len(item) == 1:
            (title, value) = list(item.items())[0]
            if isinstance(title, str):
                if isinstance(value, str):
                    return MetaNavItem(value, title)
                elif isinstance(value, list):
                    return MetaNavItem([MetaNavItem.from_yaml(it, context) for it in value], title)

        raise TypeError("Invalid nav item format {type} [{context}]".format(type=item, context=context))


class RestType(Enum):
    GLOB = "glob"
    REGEX = "regex"
    ALL = "all"


class MetaNavRestItem(MetaNavItem):
    _REGEX = r"^\.{3}\s*(?:\|\s*(flat)\s*)?\s*(?:\|\s*(?:(regex|glob)=)?(.*))?"

    def __init__(self, value: str):
        super().__init__(value)

        match = re.search(self._REGEX, value)
        if match.group(2) is not None:
            self.type = RestType(match.group(2))
        elif match.group(3) is not None:
            self.type = RestType.GLOB
        else:
            self.type = RestType.ALL

        self.pattern = match.group(3)
        self.flat = match.group(1) is not None

    def matches(self, path: Optional[str]) -> bool:
        if self.type == RestType.GLOB:
            return path is not None and glob.globmatch(path, self.pattern, flags=glob.GLOBSTAR)
        elif self.type == RestType.REGEX:
            return path is not None and re.search(self.pattern, PurePath(path).as_posix()) is not None
        else:
            return True

    @staticmethod
    def is_rest(item: Any) -> bool:
        return isinstance(item, str) and re.search(MetaNavRestItem._REGEX, item)


class RestItemList(collections.abc.Iterable):
    def __init__(self):
        self.patterns = []
        self.all = None

    def append(self, item: MetaNavRestItem):
        if item.type == RestType.ALL:
            self.all = item
        else:
            self.patterns.append(item)

    def __iter__(self) -> Iterator[MetaNavRestItem]:
        yield from self.patterns
        if self.all:
            yield self.all

    def __len__(self):
        return len(self.patterns) + (1 if self.all is not None else 0)


class Meta:
    TITLE_ATTRIBUTE = "title"
    NAV_ATTRIBUTE = "nav"
    ARRANGE_ATTRIBUTE = "arrange"
    ARRANGE_REST_TOKEN = "..."
    COLLAPSE_ATTRIBUTE = "collapse"
    COLLAPSE_SINGLE_PAGES_ATTRIBUTE = "collapse_single_pages"
    FORCE_COLLAPSE_ATTRIBUTE = "force_collapse"
    HIDE_ATTRIBUTE = "hide"
    ORDER_ATTRIBUTE = "order"
    SORT_TYPE_ATTRIBUTE = "sort_type"
    ORDER_BY_ATTRIBUTE = "order_by"

    ORDER_ASC = "asc"
    ORDER_DESC = "desc"
    SORT_NATURAL = "natural"
    ORDER_BY_FILENAME = "filename"
    ORDER_BY_TITLE = "title"

    def __init__(
        self,
        *,
        title: Optional[str] = None,
        arrange: Optional[List[str]] = None,
        nav: Optional[List[MetaNavItem]] = None,
        path: Optional[str] = None,
        collapse: Optional[bool] = None,
        collapse_single_pages: Optional[bool] = None,
        force_collapse: Optional[bool] = None,
        hide: Optional[bool] = None,
        order: Optional[str] = None,
        sort_type: Optional[str] = None,
        order_by: Optional[str] = None,
    ):
        if nav is None and arrange is not None:
            nav = [MetaNavItem.from_yaml(value, path) for value in arrange]
            if MetaNavRestItem("...") not in nav:
                nav.append(MetaNavRestItem("..."))

        self.title = title
        self.nav = nav
        self.path = path
        self.collapse = collapse
        self.collapse_single_pages = collapse_single_pages
        self.force_collapse = force_collapse
        self.hide = hide
        self.order = order
        self.sort_type = sort_type
        self.order_by = order_by

    @staticmethod
    def try_load_from_files(rel_path: Optional[str], files: "Files") -> "Meta":
        if rel_path is None:
            return Meta()

        file = files.src_paths.get(rel_path)
        if file is None:
            return Meta(path=rel_path)

        try:
            meta = Meta.load_from(file.abs_src_path)
            meta.path = file.src_path  # Use the relative path
            return meta
        except FileNotFoundError:
            return Meta(path=file.src_path)

    @staticmethod
    def load_from(path: str) -> "Meta":
        with open(path, encoding="utf-8") as file:
            contents = yaml.safe_load(file) or {}
            title = contents.get(Meta.TITLE_ATTRIBUTE)
            arrange = contents.get(Meta.ARRANGE_ATTRIBUTE)
            nav = contents.get(Meta.NAV_ATTRIBUTE)
            collapse = contents.get(Meta.COLLAPSE_ATTRIBUTE)
            collapse_single_pages = contents.get(Meta.COLLAPSE_SINGLE_PAGES_ATTRIBUTE)
            force_collapse = contents.get(Meta.FORCE_COLLAPSE_ATTRIBUTE)
            hide = contents.get(Meta.HIDE_ATTRIBUTE)
            order = contents.get(Meta.ORDER_ATTRIBUTE)
            sort_type = contents.get(Meta.SORT_TYPE_ATTRIBUTE)
            order_by = contents.get(Meta.ORDER_BY_ATTRIBUTE)

            if title is not None:
                if not isinstance(title, str):
                    raise TypeError(
                        'Expected "{attribute}" attribute to be a string - got {type} [{context}]'.format(
                            attribute=Meta.TITLE_ATTRIBUTE,
                            type=type(title),
                            context=path,
                        )
                    )
            if arrange is not None:
                if not isinstance(arrange, list) or not all(isinstance(s, str) for s in arrange):
                    raise TypeError(
                        'Expected "{attribute}" attribute to be a list of strings - got {type} [{context}]'.format(
                            attribute=Meta.ARRANGE_ATTRIBUTE,
                            type=type(arrange),
                            context=path,
                        )
                    )
                if arrange.count(Meta.ARRANGE_REST_TOKEN) > 1:
                    raise DuplicateRestItemError("...", path)

            if nav is not None:
                if not isinstance(nav, list):
                    raise TypeError(
                        'Expected "{attribute}" attribute to be a list - got {type} [{context}]'.format(
                            attribute=Meta.NAV_ATTRIBUTE, type=type(nav), context=path
                        )
                    )

                nav = [MetaNavItem.from_yaml(item, path) for item in nav]
                checked = set()
                for item in nav:
                    if isinstance(item, MetaNavRestItem):
                        if item in checked:
                            raise DuplicateRestItemError(item.value, path)
                        checked.add(item)

            if collapse is not None:
                if not isinstance(collapse, bool):
                    raise TypeError(
                        'Expected "{attribute}" attribute to be a boolean - got {type} [{context}]'.format(
                            attribute=Meta.COLLAPSE_ATTRIBUTE,
                            type=type(collapse),
                            context=path,
                        )
                    )
            if collapse_single_pages is not None:
                if not isinstance(collapse_single_pages, bool):
                    raise TypeError(
                        'Expected "{attribute}" attribute to be a boolean - got {type} [{context}]'.format(
                            attribute=Meta.COLLAPSE_SINGLE_PAGES_ATTRIBUTE,
                            type=type(collapse_single_pages),
                            context=path,
                        )
                    )

            if force_collapse is not None:
                if not isinstance(force_collapse, bool):
                    raise TypeError(
                        'Expected "{attribute}" attribute to be a boolean - got {type} [{context}]'.format(
                            attribute=Meta.FORCE_COLLAPSE_ATTRIBUTE,
                            type=type(force_collapse),
                            context=path,
                        )
                    )

            if hide is not None:
                if not isinstance(hide, bool):
                    raise TypeError(
                        'Expected "{attribute}" attribute to be a boolean - got {type} [{context}]'.format(
                            attribute=Meta.COLLAPSE_ATTRIBUTE,
                            type=type(hide),
                            context=path,
                        )
                    )
            if order is not None:
                if order != Meta.ORDER_ASC and order != Meta.ORDER_DESC:
                    raise TypeError(
                        'Expected "{attribute}" attribute to be either "desc" or "asc" - got "{order}" [{context}]'.format(
                            attribute=Meta.ORDER_ATTRIBUTE, order=order, context=path
                        )
                    )
            if sort_type is not None:
                if sort_type != Meta.SORT_NATURAL:
                    raise TypeError(
                        'Expected "{attribute}" to be "natural" - got "{sort_type}" [{context}]'.format(
                            attribute=Meta.SORT_TYPE_ATTRIBUTE, sort_type=sort_type, context=path
                        )
                    )

            if order_by is not None:
                if order_by != Meta.ORDER_BY_TITLE and order_by != Meta.ORDER_BY_FILENAME:
                    raise TypeError(
                        'Expected "{attribute}" attribute to be one of {those} - got "{order_by}" [{context}]'.format(
                            attribute=Meta.ORDER_BY_ATTRIBUTE,
                            those=[
                                Meta.ORDER_BY_FILENAME,
                                Meta.ORDER_BY_TITLE,
                            ],
                            order_by=order_by,
                            context=path,
                        )
                    )

            return Meta(
                title=title,
                arrange=arrange,
                nav=nav,
                path=path,
                collapse=collapse,
                collapse_single_pages=collapse_single_pages,
                force_collapse=force_collapse,
                hide=hide,
                order=order,
                sort_type=sort_type,
                order_by=order_by,
            )
