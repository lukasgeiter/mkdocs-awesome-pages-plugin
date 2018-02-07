import io
from unittest import TestCase
from typing import Optional

from .. import markdown


class TestExtractH1(TestCase):

    def _check(self, string: str, expected: Optional[str]):
        self.assertEqual(markdown.extract_h1(io.StringIO(string)), expected)

    def test_single_line(self):
        self._check('# Foo Bar', 'Foo Bar')

    def test_single_line_lf(self):
        self._check('# Foo Bar\n', 'Foo Bar')

    def test_single_line_crlf(self):
        self._check('# Foo Bar\r\n', 'Foo Bar')

    def test_leading_space(self):
        self._check('#   Foo Bar', 'Foo Bar')

    def test_leading_space_before_hash(self):
        self._check(' # Foo Bar', None)

    def test_trailing_space(self):
        self._check('# Foo Bar    ', 'Foo Bar')

    def test_with_other_content(self):
        self._check('# Foo Bar\n\nLorem Ipsum', 'Foo Bar')

    def test_content_before(self):
        self._check('description: Lorem Ipsum dolor\n\n# Foo Bar', 'Foo Bar')

    def test_other_heading_before(self):
        self._check('## Foo\n# Foo Bar', 'Foo Bar')

    def test_multiple_h1(self):
        self._check('# Foo Bar\n\n# Bar Foo', 'Foo Bar')

    def test_hash_in_h1(self):
        self._check('# Foo # Bar', 'Foo # Bar')

    def test_no_h1(self):
        self._check('Foo Bar', None)
