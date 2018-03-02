import os
from typing import List, Optional, Union, Dict


class Page:

    def __init__(self, title: Optional[str], path: Optional[str], children: Optional[List['Page']] = None,
                 *, collapse_single_pages: bool = None, collapse: bool = None):

        self.title = title
        self.path = path
        self.dirname = os.path.dirname(path) if path else None
        self.basename = os.path.basename(path) if path else None
        self.children = children or []
        self.collapse = collapse
        self.collapse_single_pages = collapse_single_pages

    def _children_to_mkdocs(self, collapse_single_children: bool = False) -> List:
        return list(map(lambda child: child.to_mkdocs(collapse_single_children), self.children))

    def to_mkdocs(self, collapse_single_pages: bool = False) -> Union[List, Dict, str]:
        if self.collapse_single_pages is not None:
            collapse_single_pages = self.collapse_single_pages

        collapse = self.collapse if self.collapse is not None else collapse_single_pages

        if self.children:
            children = self._children_to_mkdocs(collapse_single_pages)
            if collapse and len(children) == 1:
                return children[0]
            else:
                return {
                    self.title: children
                }
        elif self.title:
            return {
                self.title: self.path
            }
        else:
            return self.path


class RootPage(Page):

    def __init__(self, children: List[Page], collapse_single_pages: bool = False):
        super().__init__(None, '', children, collapse_single_pages=collapse_single_pages)

    def to_mkdocs(self, collapse_single_pages: bool = None) -> List:
        if collapse_single_pages is None:
            collapse_single_pages = self.collapse_single_pages
        return self._children_to_mkdocs(collapse_single_pages)
