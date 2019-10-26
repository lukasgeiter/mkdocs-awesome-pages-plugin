class Options:
    def __init__(self, *, filename: str,
                         collapse_single_pages: bool,
                         maximum_file_homepage: int,
                         maximum_days_ahead: int):
        self.filename = filename
        self.collapse_single_pages = collapse_single_pages
        self.maximum_file_homepage = maximum_file_homepage
        self.maximum_days_ahead = maximum_days_ahead
