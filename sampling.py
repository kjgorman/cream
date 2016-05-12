import numpy as np

sample_minimum = -200
sample_maximum = 200

def sample_between(lo, hi):
    lo = max(sample_minimum, lo)
    hi = min(sample_maximum, hi)

    return np.random.uniform(lo, hi)


def sample_fourier(size):
    result = np.ndarray((size), dtype="complex")
    # result[0] = mean
    # result[:size/2] = monotonic positive
    # result[size/2:] = monotonic negative

    currentMin = 0
    for ix in xrange(1, size / 2):
        sampled = np.random.uniform(currentMin, sample_maximum)
        result[ix] = sampled
        currentMin = sampled

    currentMax = 0
    for ix in xrange(size / 2, size):
        sampled = np.random.uniform(sample_minimum, currentMax)
        result[ix] = sampled
        currentMax = sampled

    result[0] = np.mean(result[1:])
    return result
