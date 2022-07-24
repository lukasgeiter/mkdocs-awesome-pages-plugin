from .base import E2ETestCase


class TestOrderAndSort(E2ETestCase):
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

    def test_asc_natural(self):
        navigation = self.mkdocs(
            self.config,
            [
                "100.md",
                "3.md",
                ("20", ["100.md", "20.md", self.pagesFile(order="asc", sort_type="natural")]),
                self.pagesFile(order="asc", sort_type="natural"),
            ],
        )

        self.assertEqual(
            navigation,
            [("3", "/3"), ("20", [("20", "/20/20"), ("100", "/20/100")]), ("100", "/100")],
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

    def test_desc_natural(self):
        navigation = self.mkdocs(
            self.config,
            [
                "100.md",
                "3.md",
                ("20", ["100.md", "20.md", self.pagesFile(order="desc", sort_type="natural")]),
                self.pagesFile(order="desc", sort_type="natural"),
            ],
        )

        self.assertEqual(
            navigation,
            [("100", "/100"), ("20", [("100", "/20/100"), ("20", "/20/20")]), ("3", "/3")],
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

    def test_nav_asc_natural(self):
        navigation = self.mkdocs(
            self.config,
            [
                "100.md",
                "3.md",
                (
                    "20",
                    ["1.md", "2.md", self.pagesFile(order="asc", sort_type="natural", nav=["2.md", "1.md"])],
                ),
                self.pagesFile(order="asc", sort_type="natural", nav=["20", "100.md", "3.md"]),
            ],
        )

        self.assertEqual(
            navigation,
            [("20", [("2", "/20/2"), ("1", "/20/1")]), ("100", "/100"), ("3", "/3")],
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

    def test_nav_desc_natural(self):
        navigation = self.mkdocs(
            self.config,
            [
                "100.md",
                "3.md",
                (
                    "20",
                    ["1.md", "2.md", self.pagesFile(order="desc", sort_type="natural", nav=["2.md", "1.md"])],
                ),
                self.pagesFile(order="desc", sort_type="natural", nav=["20", "100.md", "3.md"]),
            ],
        )

        self.assertEqual(
            navigation,
            [("20", [("2", "/20/2"), ("1", "/20/1")]), ("100", "/100"), ("3", "/3")],
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

    def test_nav_rest_asc_natural(self):
        navigation = self.mkdocs(
            self.config,
            [
                "100.md",
                "3.md",
                (
                    "20",
                    [
                        "100.md",
                        "20.md",
                        "3.md",
                        self.pagesFile(order="asc", sort_type="natural", nav=["3.md", "..."]),
                    ],
                ),
                self.pagesFile(order="asc", sort_type="natural", nav=["3.md", "..."]),
            ],
        )

        self.assertEqual(
            navigation,
            [("3", "/3"), ("20", [("3", "/20/3"), ("20", "/20/20"), ("100", "/20/100")]), ("100", "/100")],
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

    def test_nav_rest_desc_natural(self):
        navigation = self.mkdocs(
            self.config,
            [
                "100.md",
                "3.md",
                (
                    "20",
                    [
                        "100.md",
                        "20.md",
                        "3.md",
                        self.pagesFile(order="desc", sort_type="natural", nav=["3.md", "..."]),
                    ],
                ),
                self.pagesFile(order="desc", sort_type="natural", nav=["3.md", "..."]),
            ],
        )

        self.assertEqual(
            navigation,
            [
                ("3", "/3"),
                ("100", "/100"),
                ("20", [("3", "/20/3"), ("100", "/20/100"), ("20", "/20/20")]),
            ],
        )
