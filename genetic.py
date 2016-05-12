import numpy as np
import random

from partitions import halves, pairs, choose
import sampling as s

def rms_error(actual, predicted):
    cutoff = int(len(actual) * 0.05)
    cut_actual = actual[cutoff:(len(actual) - cutoff)]
    cut_predicted = predicted[cutoff:(len(predicted) - cutoff)]

    return np.sqrt(np.mean(np.square(cut_actual - cut_predicted)))

def evaluate(population, base_line):
    fitted = []

    for chromosome in population:
        fn = np.fft.ifft(chromosome)
        fitness = rms_error(base_line, fn.real)

        fitted.append((fitness, chromosome))

    fitted.sort(key=lambda x: x[0])

    return fitted

def generation(population, base_line, temperature, sampler):
    fitted = evaluate(population, base_line)
    selected, _ = halves(map(lambda l: map(lambda ll: ll.real, l[1]), fitted))
    mutated  = mutate(list(selected), temperature, sampler)

    return selected + mutated

def mutate(selection, temperature, sampler):
    random.shuffle(selection)
    first, second = halves(selection)
    return crossover(first) + mutations(second, temperature, sampler)

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

def mutations(selection, temperature, sampler):
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

                # prev should always be less if positive, unless next is negative
                # prev should always be less if negative
                edge = prev == 0 or next == 100
                sortable = (prev < 0 and next < 0) or (prev > 0 and next > 0)

                # this will turn it into a perfect square wave by correcting the
                # frequency ordering...
                if not edge and sortable:
                    mutated[i-1]    += temperature * (chromosome[i+1] - mutated[i-1])
                    chromosome[i+1] -= temperature * (chromosome[i+1] - mutated[i-1])

                mutated[i] = sampler.sample_between(prev, next)
                mutated[i] += sampler.sample_noise(temperature)
            else:
                mutated[i] = chromosome[i]

        resulting.append(mutated)

    return resulting
