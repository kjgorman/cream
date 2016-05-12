import numpy as np

sample_minimum = -1
sample_maximum = 1

def sample():
    return sample_n(sample_minimum, sample_maximum, 1)[0]

def sample_random(size):
        return [ complex(l, r) for (l, r) in
                 zip(sample_n(sample_minimum, sample_maximum, size),
                     sample_n(sample_minimum, sample_maximum, size)) ]

def sample_n(lo, hi, size):
    return np.random.uniform(lo, hi, size)
