from collections import defaultdict
from typing import TypeVar, List, Callable, Dict, Optional

from .meta import Meta


class InvalidArrangeEntry(Exception):
    def __init__(self, value: str):
        self.value = value
        super().__init__('Arrange entry "{}" is invalid.'.format(value))


T = TypeVar('T')
GetKeyCallable = Callable[[T], Optional[str]]


def arrange(entries: List[T], config: List[str], get_key: GetKeyCallable = lambda x: x) -> List[T]:
    grouped = _group(entries, get_key)
    rest_index = None
    result = []

    # Add entries in order they appear in the config
    for index, entry in enumerate(config):
        if entry == Meta.ARRANGE_REST_TOKEN:
            rest_index = index
        elif entry in grouped:
            result.extend(grouped[entry])
        else:
            raise InvalidArrangeEntry(entry)

    if rest_index is None:
        # If the configuration contains no rest token, we'll add the rest in the end
        rest_index = len(result)

    # Add entries not already part of the result at the rest_index
    result[rest_index:rest_index] = [entry for entry in entries if entry not in result]

    return result


def _group(entries: List[T], get_key: GetKeyCallable) -> Dict[str, List[T]]:
    result = defaultdict(list)
    for entry in entries:
        key = get_key(entry)

        if key is not None:
            result[key].append(entry)

    return result
