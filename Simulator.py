import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import seaborn as sns
import scipy.signal
import rd
from robot import Robot
import time
from matplotlib.animation import FuncAnimation, writers

class Simulator(object):
    """docstring for Simulator."""

    def __init__(self, nSteps, gridSize, rdParams, sideLength, shape="circle"):
        # self.a, self.b = rd.reaction_diffusion(n_steps, grid_size, rd_params)
        self.rdParams = rdParams
        self.nSteps = nSteps
        self.gridSize = gridSize
        self.sideLength = sideLength
        self.grid = self.initGrid()

    def initGrid(self):
        "returns a list of Robot objects. Based on a truncated view of self.a"
        offset = (self.gridSize - self.sideLength) // 2
        robots = np.array([[Robot(0.5,0.4 * np.random.random(),x + offset,y + offset,self.rdParams) for x in range(self.sideLength)] for y in range(self.sideLength)])

        robots[self.sideLength//2,self.sideLength//2].a += 0.1

        grid = np.zeros((self.gridSize, self.gridSize), dtype=object)
        firstInd = offset
        secondInd = firstInd + self.sideLength
        grid[firstInd:secondInd, firstInd:secondInd] = robots
        return grid

    def calcNeighbors(self, robot):
        "finds the visible neighbors of a robot. No return value"
        directions = [(0,1),(1,0),(-1,0),(0,-1)]
        neighbors = [self.grid[robot.x+x][robot.y+y] for x,y in directions if isinstance(self.grid[robot.x+x][robot.y+y], Robot)]
        robot.setNeighbors(neighbors)
        gridAround = self.grid[robot.x-1:robot.x+1][robot.y-1:robot.y+1]
        robot.setGridAround(gridAround)

    def updateSimulation(self, i):
        print(i)
        robots = []
        for gridSpace in self.grid.flatten():
            if(isinstance(gridSpace,Robot)):
                robot = gridSpace
                robots.append(robot)
                self.calcNeighbors(robot)
        for robot in robots:
            robot.updateChemicals()
            # Todo: robot.move()
        # plt.imshow(self.plottableGrid(self.grid))
        plotGrid = self.plottableGrid(self.grid)
        mask = plotGrid < 0
        with sns.axes_style("white"):
            sns.heatmap(plotGrid, mask = mask, vmax = 1, cbar=False)
        # plt.pcolormesh(self.plottableGrid(self.grid), vmin=-1, vmax=1, cmap='jet')

    def plottableGrid(self, grid):
        vectorized_grid = np.vectorize(lambda x: x.a if isinstance(x, Robot) else -1, otypes=[np.float32])
        return vectorized_grid(grid)

    def initPlot(self):
        plotGrid = self.plottableGrid(self.grid)
        mask = plotGrid < 0
        with sns.axes_style("white"):
            sns.heatmap(plotGrid, mask = mask, vmax = 1, vmin=0)


    def main(self):
        # rc('animation', html='html5')

        fig = plt.figure()
        anim = FuncAnimation(fig, self.updateSimulation, init_func=self.initPlot, frames=200, repeat=False)
        
        Writer = writers['imagemagick']
        writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
        anim.save('0.2_0.25_0.055_-0.117_200_frames.gif', writer=writer)
        # plt.show()
        


if __name__ == '__main__':
    sim = Simulator(nSteps = 1000, gridSize=60, rdParams=[0.2,0.25,0.055,-0.117],sideLength=50)
    sim.main()
