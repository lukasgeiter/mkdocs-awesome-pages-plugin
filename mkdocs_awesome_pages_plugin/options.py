class Options:
    def __init__(self, *, filename: str, collapse_single_pages: bool, hide_not_arranged_pages: bool):
        self.filename = filename
        self.collapse_single_pages = collapse_single_pages
        self.hide_not_arranged_pages = hide_not_arranged_pages
