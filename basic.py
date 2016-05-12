import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def random_lines_with_ifft():
    sample_size = 100
    x_axis = np.arange(sample_size)

    def sample_random(lo, hi, size):
        return [ complex(l, r) for (l, r) in
                 zip(np.random.uniform(lo, hi, size),
                     np.random.uniform(lo, hi, size)) ]

    def update_line(frame):
        fs = sample_random(0, 50, sample_size)
        y = np.fft.ifft(fs)

        line.set_data(x_axis, y.real)

    figure = plt.figure()
    line, = plt.plot([],[],'-r') #TODO: 'r'?

    plt.xlim(0, 100)
    plt.ylim(-20, 20)

    anim = animation.FuncAnimation(figure,
                                   update_line,
                                   25,
                                   interval=500)

    plt.show()

if __name__ == "__main__":
    random_lines_with_ifft()
