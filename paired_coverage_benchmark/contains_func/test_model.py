import numpy as np
import subject

def test_contains_func_model_cases():
    values = [1, 2, np.nan]
    assert subject.contains_func(values, 2) is True
    assert subject.contains_func(values, 4) is False
    assert subject.contains_func(values, np.nan) is True
    assert subject.contains_func([], np.nan) is False
