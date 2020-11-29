# Reaction-diffusion model
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal



def reaction_diffusion(n_steps, grid_size, ca=0.2, cb=0.25, a_add_rate=0.055, b_add_rate=-0.118, plot_on=True):
    kernel = np.array([[0, 1, 0],
                       [1, -4, 1],
                       [0, 1, 0]])

    a = 0.5 * np.ones(grid_size, dtype=float)
    b = 0.1 * np.random.random(grid_size)


    a[grid_size[0]//2, grid_size[1]//2] += 0.1

    if plot_on:
        plt.figure()
        plt.imshow(a)
        plt.colorbar()

    for step in range(n_steps):
        div_a = scipy.signal.correlate2d(a, kernel, mode='same')
        div_b = scipy.signal.correlate2d(b, kernel, mode='same')
        reaction = a * b**2
        a += div_a * ca - reaction + a_add_rate * (1-a)
        b += div_b * cb + reaction + b_add_rate * b
        print(np.max(np.max(a)), np.max(np.max(b)))

    if plot_on:
        plt.figure()
        plt.imshow(a)
        plt.colorbar()
        title = str(n_steps) + ' time steps'
        plt.title(title)

        plt.show()

if __name__ == '__main__':
    reaction_diffusion(200, (200,200), plot_on=True)
