# Reaction-diffusion model

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

kernel = np.array([[0, 1, 0],
                   [1, -4, 1],
                   [0, 1, 0]])


grid_size = 200
n_steps = 200

a = np.ones((grid_size, grid_size), dtype=float)
b = 0.1 * np.random.random((grid_size, grid_size))


a[grid_size//2,grid_size//2] += 0.1
a_add_rate = 0.055
b_add_rate = -0.055-0.062

ca = 0.2
cb = 0.25

plt.figure()
plt.imshow(a)
plt.colorbar()

for i in range(5):
    plt.figure()
    for step in range(n_steps):
        div_a = scipy.signal.correlate2d(a, kernel, mode='same')
        div_b = scipy.signal.correlate2d(b, kernel, mode='same')
        reaction = a * b**2
        a += div_a * ca - reaction + a_add_rate * (1-a)
        b += div_b * cb + reaction + b_add_rate * b

    plt.imshow(a)
    plt.colorbar()
    title = str((i + 1)* n_steps) + ' time steps'
    plt.title(title)
# plt.figure()
#
# plt.imshow(b)
# plt.colorbar()

plt.show()
