# Reaction-diffusion model
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal



def reaction_diffusion(n_steps, grid_size, ca=0.2, cb=0.25, a_add_rate=0.055, b_add_rate=-0.118, plot_on=True):
    kernel = np.array([[.05, .2, .05],
                       [ .2, -1, .2],
                       [.05, .2, .05]])

    a = np.ones(grid_size, dtype=float)
    b = 0.2 * np.random.random(grid_size)

    spx = grid_size[0]//2
    spy = grid_size[1]//2
    # r=grid_size[0] // 20
    # b[spx-r:spx+r, spy-r:spy+r] += 0.1
    r=grid_size[0] // 8
    b[spx-r:spx+r, spy-r:spy+r] *= 0.1
    # b[r:r+r, r:r+r] += 0.1
    if plot_on:
        plt.figure()
        plt.imshow(b)
        plt.colorbar()

    for step in range(n_steps):
        div_a = scipy.signal.correlate2d(a, kernel, mode='same')
        div_b = scipy.signal.correlate2d(b, kernel, mode='same')
        reaction = a * b**2
        a += div_a * ca - reaction + a_add_rate * (1-a)
        b += div_b * cb + reaction + b_add_rate * b
        # print(np.max(np.max(a)), np.max(np.max(b)))

    if plot_on:
        plt.figure()
        plt.imshow(b)
        plt.colorbar()
        title = str(n_steps) + ' time steps'
        plt.title(title)

        # plt.show()

if __name__ == '__main__':
    for nsteps in [10000]:
        # reaction_diffusion(nsteps, (50,50), ca=0.4, cb=0.2, a_add_rate=0.039, b_add_rate=-0.104, plot_on=True)
        # reaction_diffusion(nsteps, (50,50), ca=0.4, cb=0.2, a_add_rate=0.039, b_add_rate=-0.104, plot_on=True)
        reaction_diffusion(nsteps, (50,50), ca=0.4, cb=0.2, a_add_rate=0.055, b_add_rate=-0.117, plot_on=True)
    plt.show()
