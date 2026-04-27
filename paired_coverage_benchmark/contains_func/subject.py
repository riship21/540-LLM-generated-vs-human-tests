import numpy as np

def contains_func(values, key):
    if isinstance(key, float) and np.isnan(key):
        return any(np.isnan(v) for v in values)
    return key in values
