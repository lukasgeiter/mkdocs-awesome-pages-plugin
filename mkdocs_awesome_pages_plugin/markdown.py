import re
from typing import TextIO, Optional


def extract_h1(file: TextIO) -> Optional[str]:
    for line in file:
        match = re.match('#([^#].*)', line)
        if match:
            return match.group(1).strip()
