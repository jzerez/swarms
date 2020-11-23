import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import rd
from robot import Robot
from matplotlib.animation import FuncAnimation

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
        robots = np.array([[Robot(0.5,0.1,x + offset,y + offset,self.rdParams) for x in range(self.sideLength)] for y in range(self.sideLength)])

        robots[self.sideLength//2,self.sideLength//2].a += 0.1

        grid = np.zeros((self.gridSize, self.gridSize), dtype=object)
        firstInd = offset
        secondInd = firstInd + self.sideLength
        grid[firstInd:secondInd, firstInd:secondInd] = robots
        self.grid = grid

    def calcNeighbors(self, robot):
        "finds the visible neighbors of a robot. No return value"
        directions = [(0,1),(1,0),(-1,0),(0,-1)]
        neighbors = [self.grid[robot.x+x][robot.y+y] for x,y in directions if isinstance(self.grid[robot.x+x][robot.y+y], Robot)]
        robot.setNeighbors(neighbors)

    def updateSimulation(self):
        for gridSpace in self.grid.flatten():
            if(isinstance(gridSpace,Robot)):
                self.calcNeighbors(gridSpace)
                gridSpace.updateChemicals()
            # Todo: robot.move()
        plt.imshow(self.plottableGrid(self.grid))

    def plottableGrid(self, grid):
        plotGrid = grid
        plotGrid[np.where(not isinstance(grid, Robot))] = -1
        return plotGrid

    def initPlot(self):
        plt.imshow(self.plottableGrid(self.grid))


    def main(self):
        fig = plt.figure()
        anim = FuncAnimation(fig, self.updateSimulation, init_func=self.initPlot, frames=20, repeat=False)
        plt.show()
        # while(True):
        #     self.updateSimulation()

if __name__ == '__main__':
    sim = Simulator(nSteps = 1000, gridSize=100, rdParams=[0.2,0.5,0.055,-0.117],sideLength=50)
    sim.main()
