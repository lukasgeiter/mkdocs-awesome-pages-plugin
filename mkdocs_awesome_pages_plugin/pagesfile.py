import yaml
from typing import Optional, List


class DuplicateRestTokenError(Exception):
    def __init__(self, context: str = None):
        message = 'Rest token "..." is only allowed once'
        if context:
            message += ' [{context}]'

        super().__init__(message.format(context=context))


class PagesFile:

    TITLE_ATTRIBUTE = 'title'
    ARRANGE_ATTRIBUTE = 'arrange'
    ARRANGE_REST_TOKEN = '...'
    COLLAPSE_ATTRIBUTE = 'collapse'
    COLLAPSE_SINGLE_PAGES_ATTRIBUTE = 'collapse_single_pages'

    def __init__(self, *, title: Optional[str] = None, arrange: Optional[List[str]] = None, path: Optional[str] = None,
                 collapse: bool = None, collapse_single_pages: bool = None):

        self.title = title
        self.arrange = arrange or []
        self.path = path
        self.collapse = collapse
        self.collapse_single_pages = collapse_single_pages

    @staticmethod
    def load_from(path: str) -> 'PagesFile':
        with open(path, encoding='utf-8') as file:
            contents = yaml.load(file) or {}
            title = contents.get(PagesFile.TITLE_ATTRIBUTE)
            arrange = contents.get(PagesFile.ARRANGE_ATTRIBUTE)
            collapse = contents.get(PagesFile.COLLAPSE_ATTRIBUTE)
            collapse_single_pages = contents.get(PagesFile.COLLAPSE_SINGLE_PAGES_ATTRIBUTE)

            if title is not None:
                if not isinstance(title, str):
                    raise TypeError(
                        'Expected "{attribute}" attribute to be a string - got {type} [{context}]'
                        .format(attribute=PagesFile.TITLE_ATTRIBUTE,
                                type=type(title),
                                context=path)
                    )
            if arrange is not None:
                if not isinstance(arrange, list) or not all(isinstance(s, str) for s in arrange):
                    raise TypeError(
                        'Expected "{attribute}" attribute to be a list of strings - got {type} [{context}]'
                        .format(attribute=PagesFile.ARRANGE_ATTRIBUTE,
                                type=type(arrange),
                                context=path)
                    )
                if arrange.count(PagesFile.ARRANGE_REST_TOKEN) > 1:
                    raise DuplicateRestTokenError(path)
            if collapse is not None:
                if not isinstance(collapse, bool):
                    raise TypeError(
                        'Expected "{attribute}" attribute to be a boolean - got {type} [{context}]'
                        .format(attribute=PagesFile.COLLAPSE_ATTRIBUTE,
                                type=type(collapse),
                                context=path)
                    )
            if collapse_single_pages is not None:
                if not isinstance(collapse_single_pages, bool):
                    raise TypeError(
                        'Expected "{attribute}" attribute to be a boolean - got {type} [{context}]'
                        .format(attribute=PagesFile.COLLAPSE_SINGLE_PAGES_ATTRIBUTE,
                                type=type(collapse_single_pages),
                                context=path)
                    )

            return PagesFile(title=title, arrange=arrange, path=path,
                             collapse=collapse, collapse_single_pages=collapse_single_pages)
