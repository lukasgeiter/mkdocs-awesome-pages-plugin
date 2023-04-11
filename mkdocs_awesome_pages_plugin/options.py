class Options:
    def __init__(
        self,
        *,
        filename: str,
        collapse_single_pages: bool,
        strict: bool,
        order: str = None,
        sort_type: str = None,
        order_by: str = None,
    ):
        self.filename = filename
        self.collapse_single_pages = collapse_single_pages
        self.strict = strict
        self.order = order
        self.sort_type = sort_type
        self.order_by = order_by
