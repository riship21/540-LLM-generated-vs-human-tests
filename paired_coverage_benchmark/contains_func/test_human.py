import numpy as np
import subject

def test_contains_func_basic_and_nan():
    values = [1, 2, np.nan]
    assert subject.contains_func(values, 2) is True
    assert subject.contains_func(values, 5) is False
    assert subject.contains_func(values, np.nan) is True
