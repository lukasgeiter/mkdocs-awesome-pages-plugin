from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation as MkDocsNavigation

from .navigation import AwesomeNavigation
from .options import Options


class AwesomePagesPlugin(BasePlugin):

    DEFAULT_META_FILENAME = '.pages'

    config_scheme = (
        ('filename', config_options.Type(str, default=DEFAULT_META_FILENAME)),
        ('collapse_single_pages', config_options.Type(bool, default=False)),
        ('strict', config_options.Type(bool, default=True))
    )

    def on_nav(self, nav: MkDocsNavigation, config: Config, files: Files):
        return AwesomeNavigation(nav, Options(**self.config), config['docs_dir']).to_mkdocs()
