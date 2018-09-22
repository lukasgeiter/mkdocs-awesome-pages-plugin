from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation as MkDocsNavigation

from .navigation import AwesomeNavigation
from .options import Options


class AwesomePagesPlugin(BasePlugin):

    DEFAULT_META_FILENAME = '.pages'

    config_scheme = (
        ('filename', config_options.Type(mkdocs_utils.string_types, default=DEFAULT_META_FILENAME)),
        ('collapse_single_pages', config_options.Type(bool, default=False))
    )

    def on_nav(self, nav: MkDocsNavigation, config: Config, files: Files):
        return AwesomeNavigation(nav, Options(**self.config)).to_mkdocs()
