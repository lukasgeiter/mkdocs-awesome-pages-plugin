from mock_open import MockOpen


class FileMock(MockOpen):
    def _mock_call(self, path: str, mode: str = "r", *args, **kws):
        original_side_effect = self._mock_side_effect

        if path not in self._MockOpen__files:
            self._mock_side_effect = FileNotFoundError

        child = MockOpen._mock_call(self, path, mode, *args, **kws)

        self._mock_side_effect = original_side_effect
        return child
