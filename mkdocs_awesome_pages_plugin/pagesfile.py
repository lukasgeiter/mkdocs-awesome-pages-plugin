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

    def __init__(self, *, title: Optional[str] = None, arrange: Optional[List[str]] = None, path: Optional[str] = None):
        self.title = title
        self.arrange = arrange or []
        self.path = path

    @staticmethod
    def load_from(path: str) -> 'PagesFile':
        with open(path) as file:
            contents = yaml.load(file) or {}
            title = contents.get(PagesFile.TITLE_ATTRIBUTE)
            arrange = contents.get(PagesFile.ARRANGE_ATTRIBUTE)

            if title is not None:
                if not isinstance(title, str):
                    raise TypeError(
                        'Expected "{attribute}" attribute to be a string - got {type} [{context}]'
                        .format(attribute=PagesFile.TITLE_ATTRIBUTE, type=type(title), context=path)
                    )
            if arrange is not None:
                if not isinstance(arrange, list) or not all(isinstance(s, str) for s in arrange):
                    raise TypeError(
                        'Expected "arrange" attribute to be a list of strings - got {type} [{context}]'
                        .format(attribute=PagesFile.ARRANGE_ATTRIBUTE, type=type(arrange), context=path)
                    )
                if arrange.count(PagesFile.ARRANGE_REST_TOKEN) > 1:
                    raise DuplicateRestTokenError(path)

            return PagesFile(title=title, arrange=arrange, path=path)
