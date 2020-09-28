import os
import tempfile
import warnings
from typing import Optional, List, Tuple, Union, Dict
from unittest import TestCase

import pkg_resources
import yaml
from bs4 import BeautifulSoup

from ...utils import cd


class E2ETestCase(TestCase):
    MIN_ROOT_ITEMS = 2
    DUMMY_NAME = '__dummy__'

    def setUp(self):
        self.config = self.createConfig()

    def pagesFile(self, title: Optional[str] = None, arrange: Optional[List[str]] = None,
                  collapse: bool = None, collapse_single_pages: bool = None, hide: bool = None) -> Tuple[str, str]:

        data = self._removeDictNoneValues({
            'title': title,
            'arrange': arrange,
            'collapse': collapse,
            'collapse_single_pages': collapse_single_pages,
            'hide': hide
        })

        return '.pages', yaml.dump(data)

    def createConfig(self, filename: Optional[str] = None, collapse_single_pages: Optional[bool] = None,
                     mkdocs_nav: Optional[List[Union[str, Dict[str, Union[str, list]]]]] = None,
                     strict: Optional[bool] = None) -> dict:

        plugin_options = self._removeDictNoneValues({
            'filename': filename,
            'collapse_single_pages': collapse_single_pages,
            'strict': strict
        })
        plugins_entry = 'awesome-pages'
        if plugin_options:
            plugins_entry = {
                plugins_entry: plugin_options
            }

        if mkdocs_nav is not None:
            # mkdocs requires a minimum amount of top-level items to render the navigation properly
            # ensure that this requirement is met by adding dummy pages
            self._addDummyPages(mkdocs_nav, self.MIN_ROOT_ITEMS - len(mkdocs_nav))

        return {
            'plugins': [
                plugins_entry
            ],
            'nav': mkdocs_nav
        }

    def mkdocs(self, config: dict, files: List[Union[str, Tuple[str, Union[str, list]]]]):
        # mkdocs requires a minimum amount of top-level items to render the navigation properly
        # ensure that this requirement is met by adding dummy pages
        self._addDummyPages(files, self.MIN_ROOT_ITEMS)

        with tempfile.TemporaryDirectory() as temp_directory, cd(temp_directory):
            self._writeToFile('mkdocs.yml', yaml.dump(config))
            self._createFiles('docs', files)

            self._mkdocsBuild(
                config_file='mkdocs.yml',
                site_dir='dist',
                docs_dir='docs',
                site_name='E2E Tests',
                strict=True
            )

            # extract from 404 page because it's always generated and contains the navigation as well
            nav = self._extractNav('dist/404.html')
            # filter out dummy pages
            return [item for item in nav
                    if not (isinstance(item[1], str) and item[1].startswith('/' + self.DUMMY_NAME))]

    def _addDummyPages(self, items: list, number_of_pages: int):
        items.extend(['{}{}.md'.format(self.DUMMY_NAME, i) for i in range(number_of_pages)])

    def _createFiles(self, directory: str, files: List[Union[str, Tuple[str, Union[str, list]]]]):
        os.makedirs(directory, exist_ok=True)
        for file in files:
            if isinstance(file, str):
                file = (file, '')

            path = os.path.join(directory, file[0])
            contents = file[1]
            if isinstance(contents, str):
                self._writeToFile(path, contents)
            elif isinstance(contents, list):
                self._createFiles(path, contents)

    def _mkdocsBuild(self, **options):
        # register project with pkg_resources so mkdocs picks it up as a plugin (before mkdocs module import!)
        self._registerPluginDist()

        from mkdocs.commands.build import build
        from mkdocs.config import load_config

        with warnings.catch_warnings():
            # ignore deprecation warnings within mkdocs
            warnings.filterwarnings('ignore', category=DeprecationWarning)

            build(load_config(**options))

    def _extractNav(self, file) -> List[Union[Tuple[str, str], list]]:
        with open(file, 'r') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        ul = soup.find('ul', class_='nav navbar-nav')

        if ul is None:
            raise Exception(
                'Navigation not found, make sure the site contains at least {} top-level navigation entries'
                .format(self.MIN_ROOT_ITEMS)
            )

        return self._parseNav(ul)

    def _parseNav(self, ul: BeautifulSoup):
        pages = list()
        for li in ul.find_all('li', recursive=False):
            if li.has_attr('class') and ('dropdown' in li['class'] or 'dropdown-submenu' in li['class']):
                contents = self._parseNav(li.find('ul'))
            else:
                contents = li.a['href'].rstrip('/')
                if contents == '/.':
                    # normalize index url
                    contents = '/'

            pages.append(
                (li.a.text.strip(), contents)
            )

        return pages

    @staticmethod
    def _registerPluginDist():
        distribution = pkg_resources.Distribution(__file__)
        entry_point = pkg_resources.EntryPoint.parse(
            'awesome-pages = mkdocs_awesome_pages_plugin.plugin:AwesomePagesPlugin',
            dist=distribution
        )
        distribution._ep_map = {'mkdocs.plugins': {'awesome-pages': entry_point}}
        pkg_resources.working_set.add(distribution)

    @staticmethod
    def _writeToFile(path: str, content: str):
        with open(path, 'w') as file:
            file.write(content)

    @staticmethod
    def _removeDictNoneValues(dictionary: dict):
        return {k: v for k, v in dictionary.items() if v is not None}
