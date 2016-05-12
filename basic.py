import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import sampling as s
import partitions as p

def random_lines_with_ifft():
    sample_size = 256
    x_axis = np.arange(sample_size)
    sampler = s.Sampler(-50, 50)

    def update_line(frame):
        fs = p.choose(sampler.sample_fourier(10000), sample_size)
        ss = sampler.sample_fourier(sample_size)
        yf = np.fft.ifft(fs)
        ys = np.fft.ifft(ss)

        first.set_data(np.arange(sample_size), yf.real)
        second.set_data(np.arange(sample_size), ys.real)

    figure = plt.figure()
    first, second = plt.plot([],[],[],[],'-r')

    plt.xlim(0, sample_size)
    plt.ylim(-200, 200)

    anim = animation.FuncAnimation(figure,
                                   update_line,
                                   25,
                                   interval=500)

    plt.show()

if __name__ == "__main__":
    random_lines_with_ifft()
