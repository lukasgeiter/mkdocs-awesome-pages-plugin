from unittest import TestCase

from mkdocs.structure.nav import Section

from ...meta import Meta
from ...navigation import AwesomeNavigation


class TestSetTitle(TestCase):
    def setUp(self):
        self.section = Section("Section", [])

    def test(self):
        AwesomeNavigation._set_title(self.section, Meta(title="Section Title"))
        self.assertEqual(self.section.title, "Section Title")

    def test_none_value(self):
        AwesomeNavigation._set_title(self.section, Meta())
        self.assertEqual(self.section.title, "Section")

    def test_empty_string_value(self):
        AwesomeNavigation._set_title(self.section, Meta(title=""))
        self.assertEqual(self.section.title, "")


class TestCollapse(TestCase):
    def setUp(self):
        self.child = Section("Child", [])
        self.parent = Section("Parent", [self.child])

    def test_default(self):
        self.assertEqual(
            AwesomeNavigation._collapse(self.parent, collapse=None, collapse_recursive=False),
            self.parent,
        )

    def test_local_false(self):
        self.assertEqual(
            AwesomeNavigation._collapse(self.parent, collapse=False, collapse_recursive=False),
            self.parent,
        )

    def test_explicit(self):
        self.assertEqual(
            AwesomeNavigation._collapse(self.parent, collapse=True, collapse_recursive=False),
            self.child,
        )

    def test_explicit_and_recursive(self):
        self.assertEqual(
            AwesomeNavigation._collapse(self.parent, collapse=True, collapse_recursive=True),
            self.child,
        )

    def test_recursive(self):
        self.assertEqual(
            AwesomeNavigation._collapse(self.parent, collapse=None, collapse_recursive=True),
            self.child,
        )

    def test_local_override_false(self):
        self.assertEqual(
            AwesomeNavigation._collapse(self.parent, collapse=False, collapse_recursive=True),
            self.parent,
        )

    def test_multiple_children(self):
        section = Section("Parent", [Section("Child 1", []), Section("Child 2", [])])

        self.assertEqual(AwesomeNavigation._collapse(section, None, False), section)
        self.assertEqual(AwesomeNavigation._collapse(section, None, True), section)
        self.assertEqual(AwesomeNavigation._collapse(section, False, False), section)
        self.assertEqual(AwesomeNavigation._collapse(section, True, False), section)
        self.assertEqual(AwesomeNavigation._collapse(section, True, True), section)
        self.assertEqual(AwesomeNavigation._collapse(section, False, True), section)
