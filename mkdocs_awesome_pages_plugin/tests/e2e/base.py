import os
import sys
import tempfile
import warnings
from typing import Dict, List, Optional, Tuple, TypeVar, Union
from unittest import TestCase

import yaml
from bs4 import BeautifulSoup
from mkdocs import __version__ as mkdocs_version
from mkdocs import plugins
from mkdocs.commands.build import build
from mkdocs.config import load_config

from ...utils import cd

if sys.version_info >= (3, 10):
    from importlib.metadata import EntryPoint
else:
    from importlib_metadata import EntryPoint

PluginBaseT = TypeVar("PluginBaseT", bound=plugins.BasePlugin)


class E2ETestCase(TestCase):
    MIN_ROOT_ITEMS = 2
    DUMMY_NAME = "__dummy__"
    PLUGINS: Tuple[PluginBaseT] = ()

    def setUp(self):
        self.config = self.createConfig()

    def pagesFile(
        self,
        title: Optional[str] = None,
        arrange: Optional[List[str]] = None,
        nav: Optional[List[Union[str, dict]]] = None,
        collapse: bool = None,
        collapse_single_pages: bool = None,
        hide: bool = None,
        order: Optional[str] = None,
        sort_type: Optional[str] = None,
        order_by: Optional[str] = None,
    ) -> Tuple[str, str]:
        data = self._removeDictNoneValues(
            {
                "title": title,
                "arrange": arrange,
                "nav": nav,
                "collapse": collapse,
                "collapse_single_pages": collapse_single_pages,
                "hide": hide,
                "order": order,
                "sort_type": sort_type,
                "order_by": order_by,
            }
        )

        return ".pages", yaml.dump(data)

    def createConfig(
        self,
        filename: Optional[str] = None,
        collapse_single_pages: Optional[bool] = None,
        mkdocs_nav: Optional[List[Union[str, Dict[str, Union[str, list]]]]] = None,
        strict: Optional[bool] = None,
        order: Optional[str] = None,
        sort_type: Optional[str] = None,
        order_by: Optional[str] = None,
    ) -> dict:
        plugin_options = self._removeDictNoneValues(
            {
                "filename": filename,
                "collapse_single_pages": collapse_single_pages,
                "strict": strict,
                "order": order,
                "sort_type": sort_type,
                "order_by": order_by,
            }
        )
        plugins_entry = "awesome-pages"
        if plugin_options:
            plugins_entry = {plugins_entry: plugin_options}
        plugins = [
            plugins_entry,
            *[class_plugin.__name__.lower() for class_plugin in getattr(type(self), "PLUGINS", [])],
        ]

        if mkdocs_nav is not None:
            # mkdocs requires a minimum amount of top-level items to render the navigation properly
            # ensure that this requirement is met by adding dummy pages
            self._addDummyPages(mkdocs_nav, self.MIN_ROOT_ITEMS - len(mkdocs_nav))

        return {"plugins": plugins, "nav": mkdocs_nav}

    def mkdocs(
        self,
        config: dict,
        files: List[Union[str, Tuple[str, Union[str, list]]]],
        dummy_pages: bool = True,
    ):
        # mkdocs requires a minimum amount of top-level items to render the navigation properly
        # ensure that this requirement is met by adding dummy pages
        if dummy_pages:
            self._addDummyPages(files, self.MIN_ROOT_ITEMS)

        with tempfile.TemporaryDirectory() as temp_directory, cd(temp_directory):
            self._writeToFile("mkdocs.yml", yaml.dump(config))
            self._createFiles("docs", files)

            self._mkdocsBuild(
                config_file="mkdocs.yml",
                site_dir="dist",
                docs_dir="docs",
                site_name="E2E Tests",
                strict=True,
            )

            # extract from 404 page because it's always generated and contains the navigation as well
            nav = self._extractNav("dist/404.html")
            # filter out dummy pages
            return [
                item for item in nav if not (isinstance(item[1], str) and item[1].startswith("/" + self.DUMMY_NAME))
            ]

    def _addDummyPages(self, items: list, number_of_pages: int):
        items.extend(["{}{}.md".format(self.DUMMY_NAME, i) for i in range(number_of_pages)])

    def _createFiles(self, directory: str, files: List[Union[str, Tuple[str, Union[str, list]]]]):
        os.makedirs(directory, exist_ok=True)
        for file in files:
            if isinstance(file, str):
                file = (file, "")

            path = os.path.join(directory, file[0])
            contents = file[1]
            if isinstance(contents, str):
                self._writeToFile(path, contents)
            elif isinstance(contents, list):
                self._createFiles(path, contents)

    def _mkdocsBuild(self, **options):
        self._patchInstalledPlugins()

        with warnings.catch_warnings():
            # ignore deprecation warnings within mkdocs
            warnings.filterwarnings("ignore", category=DeprecationWarning)

            build(load_config(**options))

    def _extractNav(self, file) -> List[Union[Tuple[str, str], list]]:
        with open(file, "r") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        ul = soup.find("ul", class_="nav navbar-nav")

        if ul is None:
            raise Exception(
                "Navigation not found, make sure the site contains at least {} top-level navigation entries".format(
                    self.MIN_ROOT_ITEMS
                )
            )

        return self._parseNav(ul)

    def _parseNav(self, ul: BeautifulSoup):
        pages = list()
        for li in ul.find_all("li", recursive=False):
            if li.has_attr("class") and ("dropdown" in li["class"] or "dropdown-submenu" in li["class"]):
                contents = self._parseNav(li.find("ul"))
            else:
                contents = li.a["href"].rstrip("/")
                if contents == "/.":
                    # normalize index url
                    contents = "/"

            pages.append((li.a.text.strip(), contents))

        return pages

    @classmethod
    def _patchInstalledPlugins(cls):
        entry_points = {
            "awesome-pages": EntryPoint(
                name="awesome-pages",
                value="mkdocs_awesome_pages_plugin.plugin:AwesomePagesPlugin",
                group="mkdocs.plugins",
            )
        }

        for class_plugin in cls.PLUGINS:
            name = class_plugin.__name__.lower()
            entry_points[name] = EntryPoint(
                name=name,
                value=f"{class_plugin.__module__}:{class_plugin.__name__}",
                group="mkdocs.plugins",
            )

        if mkdocs_version >= "1.4.0":
            from mkdocs.config.defaults import MkDocsConfig

            MkDocsConfig.plugins.installed_plugins.update(entry_points)
        else:
            _original_get_plugins = plugins.get_plugins

            def _patched_get_plugins():
                result = _original_get_plugins()
                result.update(entry_points)
                return result

            plugins.get_plugins = _patched_get_plugins

    @staticmethod
    def _writeToFile(path: str, content: str):
        with open(path, "w") as file:
            file.write(content)

    @staticmethod
    def _removeDictNoneValues(dictionary: dict):
        return {k: v for k, v in dictionary.items() if v is not None}
