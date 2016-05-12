import numpy as np
import random

from partitions import halves, pairs, choose
import sampling as s

pop_fourier = s.sample_fourier(50000)

def rms_error(actual, predicted):
    return np.sqrt(np.mean(np.square(actual - predicted)))

def evaluate(population, base_line):
    fitted = []

    for chromosome in population:
        fn = np.fft.ifft(chromosome)
        fitness = rms_error(base_line, fn.real)

        fitted.append((fitness, chromosome))

    fitted.sort(key=lambda x: x[0])

    return fitted

def generation(population, base_line):
    fitted = evaluate(population, base_line)
    selected, _ = halves(map(lambda l: map(lambda ll: ll.real, l[1]), fitted))
    mutated  = mutate(list(selected))

    return mutate(selected) + mutated

def mutate(selection):
    random.shuffle(selection)
    first, second = halves(selection)
    return crossover(first) + mutations(second)

def resample(selection): #just add a bunch of new ones completely
    width = len(selection[0])

    return [ choose(pop_fourier, width) for _ in xrange(0, len(selection)) ]

def crossover(selection):
    """
    Implements half-uniform crossover -- for each possible
    child each slot has a 50% chance of coming from each
    parent.
    """
    parents, remaining = pairs(selection)
    resulting = [] + remaining

    for l, r in parents:
        size = len(l)
        child = np.zeros(size)
        for i in xrange(0, size):
            choice = np.random.uniform(0, 1) < 0.5
            child[i] = l[i] if choice else r[i]

        resulting.append(child)

    return resulting

def mutations(selection):
    resulting = []

    for chromosome in selection:
        size = len(chromosome)
        mutated = np.zeros(size)
        for i in xrange(0, size):
            choice = np.random.uniform(0, 1) < (1.0 / 10.0)
            # mutated[i] = s.sample_around(chromosome[i]) if choice else chromosome[i]
            if choice:
                prev = mutated[i-1] if i > 0 else 0
                next = chromosome[i+1] if i < (size - 1) else 100

                mutated[i] = s.sample_between(prev, next)
            else:
                mutated[i] = chromosome[i]

        resulting.append(mutated)

    return resulting
