import tempfile
from pathlib import Path

import yaml
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File

from .base import E2ETestCase


class GeneratedFiles(BasePlugin):
    def on_pre_build(self, *args, **kwargs):
        self.src_dir = tempfile.TemporaryDirectory()

    def on_post_build(self, *args, **kwargs):
        self.src_dir.cleanup()

    def on_files(self, files, config):
        docs_dir = Path(self.src_dir.name)
        section_dir = docs_dir / "section"
        section_dir.mkdir()
        (section_dir / "2.md").touch()
        (section_dir / "3.md").touch()
        (section_dir / ".pages").write_text(yaml.dump({"arrange": ["2.md", "...", "1.md"]}))

        for file in section_dir.iterdir():
            files.append(
                File(
                    f"section/{file.name}",
                    src_dir=self.src_dir.name,
                    dest_dir=config["site_dir"],
                    use_directory_urls=config["use_directory_urls"],
                )
            )
        return files


class TestGeneratedFiles(E2ETestCase):
    PLUGINS = [GeneratedFiles]

    def test_issue78(self):
        """See https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin/issues/78."""
        navigation = self.mkdocs(
            self.config,
            [
                (
                    "section",
                    ["1.md"],
                )
            ],
        )
        self.assertEqual(
            navigation,
            [
                (
                    "Section",
                    [("2", "/section/2"), ("3", "/section/3"), ("1", "/section/1")],
                )
            ],
        )
