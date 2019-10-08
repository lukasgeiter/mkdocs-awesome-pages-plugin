from typing import List
from unittest import TestCase

from mkdocs_awesome_pages_plugin.options import Options
from ..arrange import arrange, InvalidArrangeEntry


class TestArrange(TestCase):
    abc = ['a', 'b', 'c']

    def test_empty_config(self):
        self.assertEqual(
            arrange(
                self.abc,
                [],
                Options(filename='', collapse_single_pages=False, hide_not_arranged_pages=False)
            ),
            ['a', 'b', 'c']
        )

    def test_all_in_config(self):
        self.assertEqual(
            arrange(
                self.abc,
                ['c', 'a', 'b'],
                Options(filename='', collapse_single_pages=False, hide_not_arranged_pages=False)
            ),
            ['c', 'a', 'b']
        )

    def test_some_in_config(self):
        self.assertEqual(
            arrange(
                self.abc,
                ['b'],
                Options(filename='', collapse_single_pages=False, hide_not_arranged_pages=False)
            ),
            ['b', 'a', 'c']
        )

    def test_rest_start(self):
        self.assertEqual(
            arrange(
                self.abc,
                ['...', 'b'],
                Options(filename='', collapse_single_pages=False, hide_not_arranged_pages=False)
            ),
            ['a', 'c', 'b']
        )

    def test_rest_middle(self):
        self.assertEqual(
            arrange(
                self.abc,
                ['b', '...', 'a'],
                Options(filename='', collapse_single_pages=False, hide_not_arranged_pages=False)
            ),
            ['b', 'c', 'a']
        )

    def test_rest_end(self):
        self.assertEqual(
            arrange(
                self.abc,
                ['b', '...'],
                Options(filename='', collapse_single_pages=False, hide_not_arranged_pages=False)
            ),
            ['b', 'a', 'c']
        )

    def test_empty_rest(self):
        self.assertEqual(
            arrange(
                self.abc,
                ['c', 'b', '...', 'a'],
                Options(filename='', collapse_single_pages=False, hide_not_arranged_pages=False)
            ),
            ['c', 'b', 'a']
        )

    def test_only_rest(self):
        self.assertEqual(
            arrange(
                self.abc,
                ['...'],
                Options(filename='', collapse_single_pages=False, hide_not_arranged_pages=False)
            ),
            ['a', 'b', 'c']
        )

    def test_hide_not_arranged_pages(self):
        self.assertEqual(
            arrange(
                self.abc,
                ['a', 'c'],
                Options(filename='', collapse_single_pages=False, hide_not_arranged_pages=True)
            ),
            ['a', 'c']
        )

    def test_duplicate_entry(self):
        self.assertEqual(
            arrange(
                ['a', 'b', 'a', 'c'],
                ['b', 'a', 'c'],
                Options(filename='', collapse_single_pages=False, hide_not_arranged_pages=False)
            ),
            ['b', 'a', 'a', 'c']
        )

    def test_duplicate_config_entry(self):
        self.assertEqual(
            arrange(
                self.abc,
                ['a', 'b', 'a'],
                Options(filename='', collapse_single_pages=False, hide_not_arranged_pages=False)
            ),
            ['a', 'b', 'a', 'c']
        )

    def test_key_function(self):
        a = {'id': 'a'}
        b = {'id': 'b'}
        c = {'id': 'c'}
        self.assertEqual(
            arrange([a, b, c], ['c', 'a', 'b'],
                    Options(filename='', collapse_single_pages=False, hide_not_arranged_pages=False),
                    lambda x: x['id']),
            [c, a, b]
        )

    def test_invalid_entry(self):
        with self.assertRaises(InvalidArrangeEntry):
            arrange(['a', 'b', 'c'],
                    ['b', 'c', 'a', 'd'],
                    Options(filename='', collapse_single_pages=False, hide_not_arranged_pages=False)
                    )
