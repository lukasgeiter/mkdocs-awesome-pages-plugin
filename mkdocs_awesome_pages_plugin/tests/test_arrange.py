from typing import List
from unittest import TestCase

from ..arrange import arrange, InvalidArrangeEntry


class TestArrange(TestCase):

    abc = ['a', 'b', 'c']

    def test_empty_config(self):
        self.assertEqual(
            arrange(
                self.abc,
                []
            ),
            ['a', 'b', 'c']
        )

    def test_all_in_config(self):
        self.assertEqual(
            arrange(
                self.abc,
                ['c', 'a', 'b']
            ),
            ['c', 'a', 'b']
        )

    def test_some_in_config(self):
        self.assertEqual(
            arrange(
                self.abc,
                ['b']
            ),
            ['b', 'a', 'c']
        )

    def test_rest_start(self):
        self.assertEqual(
            arrange(
                self.abc,
                ['...', 'b']
            ),
            ['a', 'c', 'b']
        )

    def test_rest_middle(self):
        self.assertEqual(
            arrange(
                self.abc,
                ['b', '...', 'a']
            ),
            ['b', 'c', 'a']
        )

    def test_rest_end(self):
        self.assertEqual(
            arrange(
                self.abc,
                ['b', '...']
            ),
            ['b', 'a', 'c']
        )

    def test_empty_rest(self):
        self.assertEqual(
            arrange(
                self.abc,
                ['c', 'b', '...', 'a']
            ),
            ['c', 'b', 'a']
        )

    def test_only_rest(self):
        self.assertEqual(
            arrange(
                self.abc,
                ['...']
            ),
            ['a', 'b', 'c']
        )

    def test_duplicate_entry(self):
        self.assertEqual(
            arrange(
                ['a', 'b', 'a', 'c'],
                ['b', 'a', 'c']
            ),
            ['b', 'a', 'a', 'c']
        )

    def test_duplicate_config_entry(self):
        self.assertEqual(
            arrange(
                self.abc,
                ['a', 'b', 'a']
            ),
            ['a', 'b', 'a', 'c']
        )

    def test_key_function(self):
        a = {'id': 'a'}
        b = {'id': 'b'}
        c = {'id': 'c'}
        self.assertEqual(
            arrange([a, b, c], ['c', 'a', 'b'], lambda x: x['id']),
            [c, a, b]
        )

    def test_invalid_entry(self):
        with self.assertRaises(InvalidArrangeEntry):
            arrange(['a', 'b', 'c'], ['b', 'c', 'a', 'd'])
