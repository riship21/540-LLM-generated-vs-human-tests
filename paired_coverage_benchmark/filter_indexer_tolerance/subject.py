import numpy as np

def _filter_indexer_tolerance(values, target, indexer, tolerance):
    distance = abs(values[indexer] - target)
    return np.where(distance <= tolerance, indexer, -1)
