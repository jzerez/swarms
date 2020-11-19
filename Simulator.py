import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import rd

class Simulator(object):
    """docstring for Simulator."""

    def __init__(self, n_steps, grid_size, rd_params, side_length):
        self.a, self.b = rd.reaction_diffusion(n_steps, grid_size, rd_params)

        self.robots = self.init_robots()

    def init_robots(self):
        "returns a list of Robot objects. Based on a truncated view of self.a"
        pass

    def calc_neighbors(self, robot):
        "finds the visible neighbors of a robot. No return value"
        neighbors = None
        robot.set_neighbors(neighbors)
        pass

    def update_simulation(self):
        for robot in self.robots:
            self.calc_neighbors(robot)
            robot.move()

    def main(self):
        while(True):
            self.update_simulation()

if __name__ == '__main__':
    sim = Simulator()
    sim.main()
