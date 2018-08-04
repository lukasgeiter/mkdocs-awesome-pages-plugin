from mkdocs import utils as mkdocs_utils, __version__ as mkdocs_version
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

from distutils.version import LooseVersion

from . import utils
from .factory import Factory
from .options import Options


class AwesomePagesPlugin(BasePlugin):

    DEFAULT_PAGES_FILENAME = '.pages'

    config_scheme = (
        ('filename', config_options.Type(mkdocs_utils.string_types, default=DEFAULT_PAGES_FILENAME)),
        ('disable_auto_arrange_index', config_options.Type(bool, default=False)),
        ('collapse_single_pages', config_options.Type(bool, default=False))
    )

    uses_mkdocs_1_or_newer = LooseVersion(mkdocs_version) >= LooseVersion('1.0')

    def on_config(self, config):

        with utils.cd(config['docs_dir']):
            options = Options(**self.config)
            pages = Factory(options).create(self._get_mkdocs_nav(config))
            self._set_mkdocs_nav(config, pages.to_mkdocs())

        return config

    def _get_mkdocs_nav(self, config):
        if self.uses_mkdocs_1_or_newer:
            return config['nav'] or []
        else:
            return config['pages']

    def _set_mkdocs_nav(self, config, nav):
        if self.uses_mkdocs_1_or_newer:
            config['nav'] = nav
        else:
            config['pages'] = nav
