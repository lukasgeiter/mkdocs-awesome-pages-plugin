import os
from typing import List, Optional, Union, Dict


class Page:

    def __init__(self, title: Optional[str], path: Optional[str], children: Optional[List['Page']] = None):
        self.title = title
        self.path = path
        self.dirname = os.path.dirname(path) if path else None
        self.basename = os.path.basename(path) if path else None
        self.children = children or []

    def _children_to_mkdocs(self, collapse_single_children: bool = False) -> List:
        return list(map(lambda child: child.to_mkdocs(collapse_single_children), self.children))

    def to_mkdocs(self, collapse_single_pages: bool = False) -> Union[List, Dict, str]:
        if self.children:
            children = self._children_to_mkdocs(collapse_single_pages)
            if collapse_single_pages and len(children) == 1:
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

    def __init__(self, children: List[Page]):
        super().__init__(None, '', children)

    def to_mkdocs(self, collapse_single_pages: bool = False) -> List:
        return self._children_to_mkdocs(collapse_single_pages)
