import os
from typing import List, Optional, Union, Dict


class Page:

    def __init__(self, title: Optional[str], path: Optional[str], children: Optional[List['Page']] = None):
        self.title = title
        self.path = path
        self.dirname = os.path.dirname(path) if path else None
        self.basename = os.path.basename(path) if path else None
        self.children = children or []

    def _children_to_config(self) -> List:
        return list(map(lambda child: child.to_config(), self.children))

    def to_config(self) -> Union[List, Dict, str]:
        if self.children:
            return {
                self.title: self._children_to_config()
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

    def to_config(self) -> List:
        return self._children_to_config()
