import numpy as np
import subject

def test_filter_indexer_tolerance_basic():
    values = np.array([10, 20, 30])
    indexer = np.array([0, 1, 2])
    target = np.array([12, 18, 50])
    tolerance = 5
    result = subject._filter_indexer_tolerance(values, target, indexer, tolerance)
    assert (result == np.array([0, 1, -1])).all()
