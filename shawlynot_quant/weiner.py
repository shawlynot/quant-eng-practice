import numpy as np
import matplotlib.pyplot as plt


def weiner_process(dt=0.1, x0=0, n=1000):
    W: np.ndarray = np.zeros(n+1)

    t = np.arange(x0, n+1)

    W[1:] = np.cumsum(np.random.normal(1, 5, n))

    return t, W

def plot_process(t, W):
    plt.plot(t, W)
    plt.xlabel("Time(t)")
    plt.ylabel("Wiener-process W(t)")
    plt.title('Wiener-process')
    plt.savefig(".cache/Weiner.png")

if __name__ == '__main__':
    time, data = weiner_process()
    plot_process(time, data)
