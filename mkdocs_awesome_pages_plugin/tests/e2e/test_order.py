from .base import E2ETestCase


class TestOrder(E2ETestCase):
    def test_asc(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                "3.md",
                ("2", ["1.md", "2.md", self.pagesFile(order="asc")]),
                self.pagesFile(order="asc"),
            ],
        )

        self.assertEqual(
            navigation,
            [("1", "/1"), ("2", [("1", "/2/1"), ("2", "/2/2")]), ("3", "/3")],
        )

    def test_desc(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                "3.md",
                ("2", ["1.md", "2.md", self.pagesFile(order="desc")]),
                self.pagesFile(order="desc"),
            ],
        )

        self.assertEqual(
            navigation,
            [("3", "/3"), ("2", [("2", "/2/2"), ("1", "/2/1")]), ("1", "/1")],
        )

    def test_nav_asc(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                "3.md",
                (
                    "2",
                    ["1.md", "2.md", self.pagesFile(order="asc", nav=["2.md", "1.md"])],
                ),
                self.pagesFile(order="asc", nav=["2", "1.md", "3.md"]),
            ],
        )

        self.assertEqual(
            navigation,
            [("2", [("2", "/2/2"), ("1", "/2/1")]), ("1", "/1"), ("3", "/3")],
        )

    def test_nav_desc(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                "3.md",
                (
                    "2",
                    [
                        "1.md",
                        "2.md",
                        self.pagesFile(order="desc", nav=["2.md", "1.md"]),
                    ],
                ),
                self.pagesFile(order="desc", nav=["2", "1.md", "3.md"]),
            ],
        )

        self.assertEqual(
            navigation,
            [("2", [("2", "/2/2"), ("1", "/2/1")]), ("1", "/1"), ("3", "/3")],
        )

    def test_nav_rest_asc(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                "3.md",
                (
                    "2",
                    [
                        "1.md",
                        "2.md",
                        "3.md",
                        self.pagesFile(order="asc", nav=["3.md", "..."]),
                    ],
                ),
                self.pagesFile(order="asc", nav=["3.md", "..."]),
            ],
        )

        self.assertEqual(
            navigation,
            [
                ("3", "/3"),
                ("1", "/1"),
                ("2", [("3", "/2/3"), ("1", "/2/1"), ("2", "/2/2")]),
            ],
        )

    def test_nav_rest_desc(self):
        navigation = self.mkdocs(
            self.config,
            [
                "1.md",
                "3.md",
                (
                    "2",
                    [
                        "1.md",
                        "2.md",
                        "3.md",
                        self.pagesFile(order="desc", nav=["1.md", "..."]),
                    ],
                ),
                self.pagesFile(order="desc", nav=["1.md", "..."]),
            ],
        )

        self.assertEqual(
            navigation,
            [
                ("1", "/1"),
                ("3", "/3"),
                ("2", [("1", "/2/1"), ("3", "/2/3"), ("2", "/2/2")]),
            ],
        )
