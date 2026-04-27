import numpy as np
import subject

class Dummy:
    def __init__(self, value):
        self.value = value
    def copy(self):
        return Dummy(self.value)

def test_handle_no_match_returns_correct_object():
    obj = Dummy(5)
    mask = np.array([False, False, False])

    result = subject.handle_no_match(mask, obj, inplace=True)
    assert result[0] is obj

    result = subject.handle_no_match(mask, obj, inplace=False)
    assert result[0] is not obj
    assert result[0].value == obj.value
