from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

from . import utils
from .factory import Factory


class AwesomePagesPlugin(BasePlugin):

    DEFAULT_PAGES_FILENAME = '.pages'

    config_scheme = (
        ('filename', config_options.Type(mkdocs_utils.string_types, default=DEFAULT_PAGES_FILENAME)),
        ('disable_auto_arrange_index', config_options.Type(bool, default=False))
    )

    def on_config(self, config):

        with utils.cd(config['docs_dir']):
            pages = Factory(**self.config).create(config['pages'])
            config['pages'] = pages.to_config()

        return config
