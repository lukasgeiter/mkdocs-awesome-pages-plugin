class Options:
    def __init__(self, *, filename: str, disable_auto_arrange_index: bool, collapse_single_pages: bool):
        self.filename = filename
        self.disable_auto_arrange_index = disable_auto_arrange_index
        self.collapse_single_pages = collapse_single_pages
