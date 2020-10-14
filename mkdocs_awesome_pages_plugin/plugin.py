from typing import List

from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files, File
from mkdocs.structure.nav import Navigation as MkDocsNavigation, get_navigation, Section, Link
from mkdocs.structure.pages import Page

from .meta import DuplicateRestTokenError, Meta
from .navigation import AwesomeNavigation, get_by_type
from .options import Options


class AwesomePagesPlugin(BasePlugin):

    DEFAULT_META_FILENAME = '.pages'
    REST_PLACEHOLDER = 'AWESOME_PAGES_REST'

    config_scheme = (
        ('filename', config_options.Type(str, default=DEFAULT_META_FILENAME)),
        ('collapse_single_pages', config_options.Type(bool, default=False)),
        ('strict', config_options.Type(bool, default=True))
    )

    def __init__(self):
        self.nav_config_with_rest = None

    def on_nav(self, nav: MkDocsNavigation, config: Config, files: Files):
        explicit_nav = nav if config['nav'] else None

        if self.nav_config_with_rest:
            # restore explicit config with rest placeholder and build nav
            config['nav'] = self.nav_config_with_rest
            explicit_nav = get_navigation(files, config)

        explicit_sections = set(get_by_type(explicit_nav, Section)) if explicit_nav else set()

        if self.nav_config_with_rest:
            _remove_files(nav.items, [page.file for page in explicit_nav.pages])
            _insert_rest(explicit_nav.items, nav.items)
            nav = explicit_nav

        return AwesomeNavigation(nav.items, Options(**self.config), config['docs_dir'], explicit_sections).to_mkdocs()

    def on_config(self, config: Config):
        if config['nav']:
            if _find_rest_token(config['nav']):
                self.nav_config_with_rest = config['nav']
                config['nav'] = None  # clear nav to prevent MkDocs from reporting files that are not included

        return config


def _find_rest_token(config) -> bool:
    stack = [config]
    found = False
    while stack:
        data = stack.pop()
        if isinstance(data, list):
            for index, element in enumerate(data):
                if element == Meta.NAV_REST_TOKEN.value:
                    if found:
                        raise DuplicateRestTokenError('mkdocs.yml')
                    data[index] = {AwesomePagesPlugin.REST_PLACEHOLDER: '/'}
                    found = True
                else:
                    stack.append(element)

        elif isinstance(data, dict):
            stack.extend(data.values())

    return found


def _remove_files(items, to_remove: List[File]):
    for item in items[:]:  # loop over a shallow copy of items so removing items doesn't break iteration
        if isinstance(item, Page) and item.file in to_remove:
            items.remove(item)
        if isinstance(item, Section):
            _remove_files(item.children, to_remove)


def _insert_rest(items, rest):
    for index, item in enumerate(items):
        if isinstance(item, Link) and item.title == AwesomePagesPlugin.REST_PLACEHOLDER:
            items[index:index + 1] = rest
            return
        if isinstance(item, Section):
            _insert_rest(item.children, rest)
