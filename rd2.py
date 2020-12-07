# Reaction-diffusion model
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
from matplotlib.animation import FuncAnimation, writers

class fuck:
    def __init__(self):
        self.n_steps = 10000
        self.steps_per_frame = 50
        self.grid_size = (50,50)
        self.ca=0.4
        self.cb=0.2
        self.a_add_rate=0.039
        self.b_add_rate=-0.104

        self.kernel = np.array([[.05, .2, .05],
                                [ .2, -1, .2],
                                [.05, .2, .05]])

        self.a = np.ones(self.grid_size, dtype=float)
        self.b = 0.1 * np.random.random(self.grid_size)

        spx = self.grid_size[0]//2
        spy = self.grid_size[1]//2
        r=self.grid_size[0] // 20
        self.b[spx-r:spx+r, spy-r:spy+r] += 0.1



    def take_step(self):
        div_a = scipy.signal.correlate2d(self.a, self.kernel, mode='same', boundary='wrap')
        div_b = scipy.signal.correlate2d(self.b, self.kernel, mode='same', boundary='wrap')
        reaction = self.a * self.b**2
        self.a += div_a * self.ca - reaction + self.a_add_rate * (1-self.a)
        self.b += div_b * self.cb + reaction + self.b_add_rate * self.b
    # print(np.max(np.max(a)), np.max(np.max(b)))

    def take_steps(self,i):
        print(i * self.steps_per_frame)
        for _ in range(self.steps_per_frame):
            self.take_step()
        plt.imshow(self.a, vmin=0, vmax=1)

    def initPlot(self):
        plt.imshow(self.a, vmin=0, vmax=1)

    def run(self):
        fig = plt.figure()
        anim = FuncAnimation(fig, self.take_steps, init_func=self.initPlot, frames=self.n_steps//self.steps_per_frame, repeat=False)
        Writer = writers['imagemagick']
        writer = Writer(fps=35, metadata=dict(artist='Me'), bitrate=1800)
        anim.save('dots1.gif', writer=writer)
if __name__ == '__main__':
    f = fuck()
    f.run()
