from unittest import TestCase

from ..page import Page, RootPage


class TestPage(TestCase):

    def test_basename_path_none(self):
        page = Page('Foo', None)
        self.assertIsNone(page.basename)

    def test_basename(self):
        page = Page('Foo', 'foo/foo.md')
        self.assertEqual(page.basename, 'foo.md')

    def test_dirname_path_none(self):
        page = Page('Foo', None)
        self.assertIsNone(page.dirname)

    def test_dirname(self):
        page = Page('Foo', 'foo/foo.md')
        self.assertEqual(page.dirname, 'foo')

    def test_to_mkdocs(self):
        page = Page('Foo', 'foo.md')
        self.assertEqual(page.to_mkdocs(), {
            'Foo': 'foo.md'
        })

    def test_to_mkdocs_no_title(self):
        page = Page(None, 'foo.md')
        self.assertEqual(page.to_mkdocs(), 'foo.md')

    def test_to_mkdocs_children(self):
        page = Page('Foo', 'foo', [
            Page('FooFoo', 'foo/foo.md'),
            Page('FooBar', 'foo/bar.md')
        ])
        self.assertEqual(page.to_mkdocs(), {
            'Foo': [
                {
                    'FooFoo': 'foo/foo.md'
                },
                {
                    'FooBar': 'foo/bar.md'
                }
            ]
        })

    def test_to_mkdocs_collapse_single_pages_disabled(self):
        page = Page('Foo', 'foo', [
            Page('FooBar', 'foo/foo.md')
        ])
        self.assertEqual(page.to_mkdocs(), {
            'Foo': [
                {
                    'FooBar': 'foo/foo.md'
                }
            ]
        })

    def test_to_mkdocs_collapse_recursive_inherited(self):
        page = Page('Foo', 'foo', [
            Page('FooBar', 'foo/bar.md')
        ])
        self.assertEqual(page.to_mkdocs(collapse_single_pages=True), {
            'FooBar': 'foo/bar.md'
        })

    def test_to_mkdocs_collapse_recursive_inherited_complex(self):
        page = Page('Foo', 'foo', [
            Page('FooBar', 'foo/bar', [
                Page('FooBarFoo', 'foo/bar/foo', [
                    Page('FooBarFooIndex', 'foo/bar/foo/index.md')
                ]),
                Page('FooBarBar', 'foo/bar/bar', [
                    Page('FooBarBarIndex', 'foo/bar/bar/index.md')
                ])
            ])
        ])
        self.assertEqual(page.to_mkdocs(collapse_single_pages=True), {
            'FooBar': [
                {
                    'FooBarFooIndex': 'foo/bar/foo/index.md'
                },
                {
                    'FooBarBarIndex': 'foo/bar/bar/index.md'
                }
            ]
        })

    def test_to_mkdocs_collapse_recursive_local(self):
        page = Page('Foo', 'foo', [
            Page('FooBar', 'foo/bar.md')
        ], collapse_single_pages=True)
        self.assertEqual(page.to_mkdocs(), {
            'FooBar': 'foo/bar.md'
        })

    def test_to_mkdocs_collapse_recursive_local_complex(self):
        page = Page('Foo', 'foo', [
            Page('FooBar', 'foo/bar', [
                Page('FooBarFoo', 'foo/bar/foo', [
                    Page('FooBarFooIndex', 'foo/bar/foo/index.md')
                ]),
                Page('FooBarBar', 'foo/bar/bar', [
                    Page('FooBarBarIndex', 'foo/bar/bar/index.md')
                ])
            ])
        ], collapse_single_pages=True)
        self.assertEqual(page.to_mkdocs(), {
            'FooBar': [
                {
                    'FooBarFooIndex': 'foo/bar/foo/index.md'
                },
                {
                    'FooBarBarIndex': 'foo/bar/bar/index.md'
                }
            ]
        })

    def test_to_mkdocs_collapse_non_recursive(self):
        page = Page('Foo', 'foo', [
            Page('FooBar', 'foo/bar.md')
        ], collapse=True)
        self.assertEqual(page.to_mkdocs(), {
            'FooBar': 'foo/bar.md'
        })

    def test_to_mkdocs_collapse_non_recursive_complex(self):
        page = Page('Foo', 'foo', [
            Page('FooBar', 'foo/bar', [
                Page('FooBarFoo', 'foo/bar/foo', [
                    Page('FooBarFooIndex', 'foo/bar/foo/index.md')
                ]),
                Page('FooBarBar', 'foo/bar/bar', [
                    Page('FooBarBarIndex', 'foo/bar/bar/index.md')
                ], collapse=True)
            ])
        ], collapse=True)
        self.assertEqual(page.to_mkdocs(), {
            'FooBar': [
                {
                    'FooBarFoo': [
                        {
                            'FooBarFooIndex': 'foo/bar/foo/index.md'
                        }
                    ]
                },
                {
                    'FooBarBarIndex': 'foo/bar/bar/index.md'
                }
            ]
        })

    def test_to_mkdocs_collapse_recursive_local_overrides_inherited(self):
        page = Page('Foo', 'foo', [
            Page('FooBar', 'foo/bar', [
                Page('FooBarFoo', 'foo/bar/foo', [
                    Page('FooBarFooIndex', 'foo/bar/foo/index.md')
                ]),
                Page('FooBarBar', 'foo/bar/bar', [
                    Page('FooBarBarIndex', 'foo/bar/bar/index.md')
                ])
            ])
        ], collapse_single_pages=False)
        self.assertEqual(page.to_mkdocs(collapse_single_pages=True), {
            'Foo': [
                {
                    'FooBar': [
                        {
                            'FooBarFoo': [
                                {
                                    'FooBarFooIndex': 'foo/bar/foo/index.md'
                                }
                            ]
                        },
                        {
                            'FooBarBar': [
                                {
                                    'FooBarBarIndex': 'foo/bar/bar/index.md'
                                }
                            ]
                        }
                    ]
                }
            ]
        })

    def test_to_mkdocs_collapse_non_recursive_overrides_recursive(self):
        page = Page('Foo', 'foo', [
            Page('FooBar', 'foo/bar.md')
        ], collapse_single_pages=True, collapse=False)
        self.assertEqual(page.to_mkdocs(), {
            'Foo': [
                {
                    'FooBar': 'foo/bar.md'
                }
            ]
        })

    def test_to_mkdocs_collapse_superfluous_local_non_recursive(self):
        page = Page('Foo', 'foo', [
            Page('FooBar', 'foo/bar', [
                Page('FooBarIndex', 'foo/bar/index.md')
            ])
        ], collapse_single_pages=True, collapse=True)
        self.assertEqual(page.to_mkdocs(), {
            'FooBarIndex': 'foo/bar/index.md'
        })

    def test_to_mkdocs_collapse_example(self):
        page = Page('Foo', 'foo', [
            Page('FooBar', 'foo/bar', [
                Page('FooBarFoo', 'foo/bar/foo', [
                    Page('FooBarFooFoo', 'foo/bar/foo/foo', [
                        Page('FooBarFooFooFoo', 'foo/bar/foo/foo/foo', [
                            Page('FooBarFooFooFooIndex', 'foo/bar/foo/foo/foo/index.md')
                        ])
                    ], collapse=False),
                    Page('FooBarFooBar', 'foo/bar/foo/bar', [
                        Page('FooBarFooBarFoo', 'foo/bar/foo/bar/foo', [
                            Page('FooBarFooBarFooIndex', 'foo/bar/foo/bar/foo/index.md')
                        ])
                    ])
                ]),
                Page('FooBarBar', 'foo/bar/bar', [
                    Page('FooBarBarFoo', 'foo/bar/bar/foo', [
                        Page('FooBarBarFooFoo', 'foo/bar/bar/foo/foo', [
                            Page('FooBarBarFooFooIndex', 'foo/bar/bar/foo/foo/index.md')
                        ])
                    ]),
                    Page('FooBarBarBar', 'foo/bar/bar/bar', [
                        Page('FooBarBarBarFoo', 'foo/bar/bar/bar/foo', [
                            Page('FooBarBarBarFooIndex', 'foo/bar/bar/bar/foo/index.md')
                        ])
                    ], collapse=True)
                ], collapse_single_pages=False)
            ])
        ])
        self.assertEqual(page.to_mkdocs(collapse_single_pages=True), {
            'FooBar': [
                {
                    'FooBarFoo': [
                        {
                            'FooBarFooFoo': [
                                {
                                    'FooBarFooFooFooIndex': 'foo/bar/foo/foo/foo/index.md'
                                }
                            ]
                        },
                        {
                            'FooBarFooBarFooIndex': 'foo/bar/foo/bar/foo/index.md'
                        }
                    ]
                },
                {
                    'FooBarBar': [
                        {
                            'FooBarBarFoo': [
                                {
                                    'FooBarBarFooFoo': [
                                        {
                                            'FooBarBarFooFooIndex': 'foo/bar/bar/foo/foo/index.md'
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'FooBarBarBarFoo': [
                                {
                                    'FooBarBarBarFooIndex': 'foo/bar/bar/bar/foo/index.md'
                                }
                            ]
                        }
                    ]
                }
            ]
        })

    def test_to_mkdocs_root(self):
        page = RootPage([
            Page('Foo', 'foo.md'),
            Page('Bar', 'bar.md')
        ])
        self.assertEqual(page.to_mkdocs(), [
            {
                'Foo': 'foo.md'
            },
            {
                'Bar': 'bar.md'
            }
        ])

    def test_to_mkdocs_collapse_root(self):
        page = RootPage([
            Page('Foo', 'foo', [
                Page('FooBar', 'foo/bar.md')
            ])
        ], collapse_single_pages=True)
        self.assertEqual(page.to_mkdocs(), [
            {
                'FooBar': 'foo/bar.md'
            }
        ])

    def test_to_mkdocs_collapse_root_argument_override(self):
        page = RootPage([
            Page('Foo', 'foo', [
                Page('FooBar', 'foo/bar.md')
            ])
        ], collapse_single_pages=True)
        self.assertEqual(page.to_mkdocs(collapse_single_pages=False), [
            {
                'Foo': [
                    {
                        'FooBar': 'foo/bar.md'
                    }
                ]
            }
        ])

    def test_to_mkdocs_empty_root(self):
        page = RootPage([])
        self.assertEqual(page.to_mkdocs(), [])

    def test_to_mkdocs_tree(self):
        tree = RootPage([
            Page('Foo', 'foo.md'),
            Page('Bar', 'bar', [
                Page(None, 'bar/index.md'),
                Page('BarBar', 'bar/bar.md')
            ])
        ])
        self.assertEqual(tree.to_mkdocs(), [
            {
                'Foo': 'foo.md'
            },
            {
                'Bar': [
                    'bar/index.md',
                    {
                        'BarBar': 'bar/bar.md'
                    }
                ]
            }
        ])
