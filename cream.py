import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from partitions import choose
import genetic  as g
import sampling as s

if __name__ == '__main__':
    width = 1536
    # pop_fouriers = [ s.sample_fourier(width) for _ in xrange(0, 5000) ]
    pop_freqs = s.sample_fourier(50000)

    # create 100 random subsamples
    population = [ choose(pop_freqs, width) for _ in xrange(0, 500) ]
    #population = choose(pop_fouriers, 100)
    base_line = 30 * np.cos((1.0 / 64) * np.arange(width))
    x_axis = np.arange(width)

    def best_error(pop):
        return g.evaluate(pop, base_line)[0][0]

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
        global line
        global previous
        epoch = 0

        while epoch < 100:
            population = g.generation(population, base_line)
            best = best_error(population)

            if epoch % 100 == 0:
                print "epoch %s \t RMSE: %s \t delta: %s" % (epoch, best, delta)
                delta = previous - best
                previous = best
            epoch += 1

        line.set_data(np.arange(width), g.evaluate(population, base_line)[0][1])

    anim = animation.FuncAnimation(figure, update_line, 50, interval=5)
    plt.show()
