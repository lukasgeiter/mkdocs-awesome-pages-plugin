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

    def test_global_asc_without_local(self):
        navigation = self.mkdocs(
            self.createConfig(order="asc"),
            [
                "1.md",
                "3.md",
                ("2", ["1.md", "2.md"]),
            ],
        )

        self.assertEqual(
            navigation,
            [("1", "/1"), ("2", [("1", "/2/1"), ("2", "/2/2")]), ("3", "/3")],
        )

    def test_global_asc_local_desc(self):
        navigation = self.mkdocs(
            self.createConfig(order="asc"),
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

    def test_global_asc_natural_without_local(self):
        navigation = self.mkdocs(
            self.createConfig(order="asc", sort_type="natural"),
            [
                "100.md",
                "3.md",
                ("20", ["100.md", "20.md"]),
            ],
        )

        self.assertEqual(
            navigation,
            [("3", "/3"), ("20", [("20", "/20/20"), ("100", "/20/100")]), ("100", "/100")],
        )

    def test_global_asc_order_by_title_without_local_h1_title(self):
        navigation = self.mkdocs(
            self.createConfig(order="asc", order_by="title"),
            [
                ("1.md", "# C"),
                ("B", [("1.md", "# C"), ("2.md", "# B")]),
                ("3.md", "# A"),
            ],
        )

        self.assertEqual(
            navigation,
            [("A", "/3"), ("B", [("B", "/B/2"), ("C", "/B/1")]), ("C", "/1")],
        )

    def test_global_asc_order_by_title_without_local_meta_title(self):
        navigation = self.mkdocs(
            self.createConfig(order="asc", order_by="title"),
            [
                ("1.md", "---\ntitle: c\n---\n"),
                ("2.md", "---\ntitle: b\n---\n"),
                ("3.md", "---\ntitle: a\n---\n"),
            ],
        )

        self.assertEqual(
            navigation,
            [("a", "/3"), ("b", "/2"), ("c", "/1")],
        )

    def test_global_asc_order_by_title_without_local_no_title(self):
        navigation = self.mkdocs(
            self.createConfig(order="asc", order_by="title"),
            [
                "1.md",
                "2.md",
                "3.md",
            ],
        )

        self.assertEqual(
            navigation,
            [("1", "/1"), ("2", "/2"), ("3", "/3")],
        )

    def test_global_asc_order_by_title_local_desc(self):
        navigation = self.mkdocs(
            self.createConfig(order="asc", order_by="title"),
            [
                ("1.md", "# C"),
                ("B", [("1.md", "# C"), ("2.md", "# B"), self.pagesFile(order="desc")]),
                ("3.md", "# A"),
                self.pagesFile(order="desc"),
            ],
        )

        self.assertEqual(
            navigation,
            [("C", "/1"), ("B", [("C", "/B/1"), ("B", "/B/2")]), ("A", "/3")],
        )

    def test_global_asc_order_by_title_local_filename(self):
        navigation = self.mkdocs(
            self.createConfig(order="asc", order_by="title"),
            [
                ("1.md", "# C"),
                ("2", [("1.md", "# C"), ("2.md", "# B"), self.pagesFile(order_by="filename")]),
                ("3.md", "# A"),
                self.pagesFile(order_by="filename"),
            ],
        )

        self.assertEqual(
            navigation,
            [("C", "/1"), ("2", [("C", "/2/1"), ("B", "/2/2")]), ("A", "/3")],
        )

    def test_local_order_by_title_without_global(self):
        navigation = self.mkdocs(
            self.createConfig(),
            [
                ("1.md", "# C"),
                ("B", [("1.md", "# C"), ("2.md", "# B"), self.pagesFile(order_by="title")]),
                ("3.md", "# A"),
                self.pagesFile(order_by="title"),
            ],
        )

        self.assertEqual(
            navigation,
            [("A", "/3"), ("B", [("B", "/B/2"), ("C", "/B/1")]), ("C", "/1")],
        )

    def test_local_order_by_title_with_global_filename(self):
        navigation = self.mkdocs(
            self.createConfig(order_by="filename"),
            [
                ("1.md", "# C"),
                ("B", [("1.md", "# C"), ("2.md", "# B"), self.pagesFile(order_by="title")]),
                ("3.md", "# A"),
                self.pagesFile(order_by="title"),
            ],
        )

        self.assertEqual(
            navigation,
            [("A", "/3"), ("B", [("B", "/B/2"), ("C", "/B/1")]), ("C", "/1")],
        )

    def test_local_order_by_inner_filename_root_title(self):
        navigation = self.mkdocs(
            self.createConfig(),
            [
                ("1.md", "# C"),
                ("B", [("1.md", "# C"), ("2.md", "# B"), self.pagesFile(order_by="filename")]),
                ("3.md", "# A"),
                self.pagesFile(order_by="title"),
            ],
        )

        self.assertEqual(
            navigation,
            [("A", "/3"), ("B", [("C", "/B/1"), ("B", "/B/2")]), ("C", "/1")],
        )

    def test_order_by_title_section_with_custom_title(self):
        navigation = self.mkdocs(
            self.createConfig(),
            [
                ("1.md", "# C"),
                ("B", [("1.md", "# C"), ("2.md", "# B"), self.pagesFile(title="D")]),
                ("3.md", "# A"),
                self.pagesFile(order_by="title"),
            ],
        )

        self.assertEqual(
            navigation,
            [("A", "/3"), ("C", "/1"), ("D", [("C", "/B/1"), ("B", "/B/2")])],
        )
