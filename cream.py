import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from partitions import choose
import genetic  as g
import sampling as s

if __name__ == '__main__':
    pop_freqs = s.sample_fourier(50000)
    stretch = 1

    # create 100 random subsamples
    width = 256
    population = [ choose(pop_freqs, width / stretch) for _ in xrange(0, 100) ]
    base_line = 20 * np.sin((1.0 / 16) * np.arange(width))
    x_axis = np.arange(width)

    def best_error(pop):
        return g.evaluate(pop, base_line, stretch)[0][0]

    delta = 10000
    previous = 10000

    figure = plt.figure()
    line, base = plt.plot([], [], x_axis, base_line)

    plt.xlim(0, width)
    plt.ylim(-200, 200)

    def update_line(frame):
        # this is stupid -- should pack it into an object
        global population
        global delta
        global base_line
        global stretch
        global line
        global previous
        epoch = 0

        while epoch < 1000:
            population = g.generation(population, base_line, stretch)
            best = best_error(population)

            if epoch % 1000 == 0:
                print "epoch %s \t RMSE: %s \t delta: %s" % (epoch, best, delta)
                delta = previous - best
                previous = best
            epoch += 1

        line.set_data(np.arange(width), g.evaluate(population, base_line, stretch)[0][1])

    anim = animation.FuncAnimation(figure, update_line, 50, interval=5)
    plt.show()
