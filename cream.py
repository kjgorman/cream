import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from partitions import choose
import genetic  as g
import sampling as s

class IterationState:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

if __name__ == '__main__':
    width = 1536
    pop_freqs = s.sample_fourier(50000)
    x_axis = np.arange(width)

    figure = plt.figure()
    base_line = 30 * np.cos((1.0 / 64) * np.arange(width))

    state = IterationState(
        population = [ choose(pop_freqs, width) for _ in xrange(0, 500) ],
        base_line = base_line,
        delta = 10000,
        previous = 10000,
        line = plt.plot([], [], x_axis, base_line)[0],
        epoch = 0)

    def best_error(pop):
        return g.evaluate(pop, base_line)[0][0]

    plt.xlim(0, width)
    plt.ylim(-200, 200)

    def update_line(frame, state):
        current = 0

        while current < 100:
            state.population = g.generation(state.population, state.base_line)
            best = best_error(state.population)

            if state.epoch % 100 == 0:
                print "epoch %s \t RMSE: %s \t delta: %s" % (state.epoch, best, state.delta)
                state.delta = state.previous - best
                state.previous = best

            state.epoch += 1
            current += 1

        state.line.set_data(
            np.arange(width), g.evaluate(state.population, state.base_line)[0][1])

    anim = animation.FuncAnimation(
        figure,
        update_line,
        50,
        interval=5,
        fargs=(state,))

    plt.show()
