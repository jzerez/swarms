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

    def __init__(self, nSteps, gridSize, rdParams, sideLength, shape="circle", stepsPerFrame=25):
        # self.a, self.b = rd.reaction_diffusion(n_steps, grid_size, rd_params)
        self.rdParams = rdParams
        self.nSteps = nSteps
        self.gridSize = gridSize
        self.sideLength = sideLength
        self.grid = self.initGrid()
        self.stepsPerFrame = stepsPerFrame

    def initGrid(self):
        "returns a list of Robot objects. Based on a truncated view of self.a"
        offset = (self.gridSize - self.sideLength) // 2
        robots = np.zeros((self.sideLength, self.sideLength), dtype=np.object)

        def inCenter(coor, r=10):
            return abs(coor - self.sideLength / 2) < self.sideLength / r

        for x in range(self.sideLength):
            for y in range(self.sideLength):
                if inCenter(x) and inCenter(y):
                    b = 0.1
                    print(x, y)
                else:
                    b = 0
                robots[x, y] = Robot(1.0, 0.1 * np.random.random() + b,x + offset,y + offset,self.rdParams)


        grid = np.zeros((self.gridSize, self.gridSize), dtype=object)
        firstInd = offset
        secondInd = firstInd + self.sideLength
        grid[firstInd:secondInd, firstInd:secondInd] = robots
        return grid

    def calcNeighbors(self, robot):
        "finds the visible neighbors of a robot. No return value"
        neighbors = self.grid[robot.x-1:robot.x+2, robot.y-1:robot.y+2]
        robot.setNeighbors(neighbors)

    def updateSimulation(self):
        robots = []
        for gridSpace in self.grid.flatten():
            if(isinstance(gridSpace,Robot)):
                robot = gridSpace
                robots.append(robot)
                self.calcNeighbors(robot)
        for robot in robots:
            robot.setDivergence()
            robot.updateChemicals()
            # Todo: robot.move()
        # plt.imshow(self.plottableGrid(self.grid))
        
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
        def updateFrame(i):
            for _ in range(self.stepsPerFrame):
                self.updateSimulation()
            plotGrid = self.plottableGrid(self.grid)
            mask = plotGrid < 0
            with sns.axes_style("white"):
                sns.heatmap(plotGrid, mask = mask, vmax = 1, cbar=False)
        
        anim = FuncAnimation(fig, updateFrame, init_func=self.initPlot, frames=self.nSteps//self.stepsPerFrame, repeat=False)

        Writer = writers['imagemagick']
        writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
        anim.save('0.4_0.2_0.039_-0.104_5000_frames.gif', writer=writer)
        # plt.show()



if __name__ == '__main__':
    sim = Simulator(nSteps = 5000, gridSize=60, rdParams=[0.4,0.2,0.039,-0.104],sideLength=50, stepsPerFrame=35)
    sim.main()
