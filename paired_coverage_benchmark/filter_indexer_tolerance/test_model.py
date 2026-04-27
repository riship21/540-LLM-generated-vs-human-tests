import numpy as np
import subject

def test_filter_indexer_tolerance_basic():
    values = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    target = 3.5
    indexer = np.array([0, 1, 2, 3, 4, 5])
    tolerance = 0.6
    expected = np.array([-1, -1, 2, 3, -1, -1])
    result = subject._filter_indexer_tolerance(values, target, indexer, tolerance)
    np.testing.assert_array_equal(result, expected)
