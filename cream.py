import numpy as np
import matplotlib.pyplot as plt

from partitions import halves, pairs, choose
import genetic as g

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

if __name__ == '__main__':
    pop_freqs = sample_random(10000)

    # create 100 random subsamples
    population = [ choose(pop_freqs, 256) for _ in xrange(0, 1000) ]
    base_line = np.sin((1.0 / 2) * np.arange(256))
    x_axis = np.arange(256)

    def best_error(pop):
        return g.evaluate(pop)[0][0]

    epoch = 0
    delta = 10000
    previous = 10000

    while best_error(population) > 0.05 and delta > 0.00001:
        population = g.generation(population, base_line)
        best = best_error(population)

        if epoch % 1000 == 0:
            print "epoch %s \t RMSE: %s \t delta: %s" % (epoch, best, delta)
            delta = previous - best
            previous = best

        epoch += 1

    best = g.evaluate(population)[0][1]

    plt.plot(x_axis, best, x_axis, base_line)
    plt.show()
