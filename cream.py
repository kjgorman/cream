import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from partitions import choose
import genetic  as g
import sampling as s
import example  as e

class IterationState:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def run_simulation(base_line, sample_min, sample_max, view_min, view_max):
    width = len(base_line) # 256 # 1536
    sampler = s.Sampler(sample_min, sample_max)
    pop_freqs = sampler.sample_fourier(50000)
    x_axis = np.arange(width)

    figure = plt.figure()

    first, second, third = plt.plot([], [], [], [], x_axis, base_line)

    left = IterationState(
        population = [ choose(pop_freqs, width) for _ in xrange(0, 2000) ],
        base_line = base_line,
        delta = 10000,
        previous = 10000,
        line = first,
        epoch = 0)

    right = IterationState(
        population = [ choose(pop_freqs, width) for _ in xrange(0, 2000) ],
        base_line = base_line,
        delta = 10000,
        previous = 10000,
        line = second,
        epoch = 0)

    plt.xlim(0, width)
    plt.ylim(view_min, view_max)

    def update_line(frame, left, right):
        update_state(left, sampler, base_line, width)
        update_state(right, sampler, base_line, width)

    anim = animation.FuncAnimation(
        figure,
        update_line,
        50,
        interval=5,
        fargs=(left, right))

    plt.show()

def update_state(state, sampler, base_line, width):
    def best_error(pop):
        return g.evaluate(pop, base_line)[0][0]

    current = 0

    while current < 100:
        # linear, but could be exponential?
        temperature = max(0, 1 - (float(state.epoch) / 10000))

        state.population = g.generation(
            state.population,
            state.base_line,
            temperature,
            sampler
        )
        best = best_error(state.population)

        if state.epoch % 100 == 0:
            print "epoch %s \t RMSE: %s \t delta: %s \t temperature %s" % (
                state.epoch,
                best,
                state.delta,
                temperature)

            state.delta = state.previous - best
            state.previous = best

        state.epoch += 1
        current += 1

    state.line.set_data(
        np.arange(width), g.evaluate(state.population, state.base_line)[0][1])

def run_sine():
    width = 256
    base_line = 30 * (np.sin((1.0 / 16) * np.arange(width)))

    run_simulation(base_line, -75, 75, -100, 100)

def run_model():
    cs = e.process_example()[60:(60+256)]
    xs, ys = e.transpose(cs)
    scale_factor = 100
    sample_min = -scale_factor
    sample_max = scale_factor

    base_line = np.asarray(ys, dtype="float")
    base_line *= scale_factor/base_line.max()
    run_simulation(base_line, sample_min, sample_max, sample_min, sample_max * 2)

if __name__ == '__main__':
    #run_model()
    run_sine()
