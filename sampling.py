import numpy as np

class Sampler():

    def __init__(self, min, max):
        self.sample_minimum = min
        self.sample_maximum = max

    def sample_noise(self, temperature):
        range = (self.sample_maximum - self.sample_minimum) * temperature
        distance = range / 2

        return self.sample_between(-distance, distance)

    def sample_between(self, lo, hi):
        lo = max(self.sample_minimum, lo)
        hi = min(self.sample_maximum, hi)

        return np.random.uniform(lo, hi)

    def sample_around(self, point):
        sample_range = self.sample_maximum - self.sample_minimum
        deviancy = 0.1 * sample_range

        return sample_between(
            max(point - deviancy, self.sample_minimum),
            min(point + deviancy, self.sample_maximum))

    def sample_fourier(self, size):
        result = np.ndarray(size, dtype="complex")
        # result[0] = mean
        # result[:size/2] = monotonic positive
        # result[size/2:] = monotonic negative

        currentMin = 0
        for ix in xrange(1, size / 2):
            sampled = np.random.uniform(currentMin, self.sample_maximum)
            result[ix] = sampled
            currentMin = sampled

            currentMax = 0
            for ix in xrange(size / 2, size):
                sampled = np.random.uniform(self.sample_minimum, currentMax)
                result[ix] = sampled
                currentMax = sampled

                result[0] = 0
                return result
