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

    def __init__(self, nSteps, gridSize, rdParams, sideLength, shape="circle", stepsPerFrame=25, stepsPerChemicalUpdate=1, stepsPerRobotMovement=5):
        # self.a, self.b = rd.reaction_diffusion(n_steps, grid_size, rd_params)
        self.rdParams = rdParams
        self.nSteps = nSteps
        self.gridSize = gridSize
        self.sideLength = sideLength

        self.movingRobot = None
        self.grid = self.initGrid()

        for robot in self.robots:
            self.calcNeighbors(robot)
        self.edgeRobots = set([robot for robot in self.robots if robot.detectEdge()])

        self.stepsPerFrame = stepsPerFrame
        self.stepsPerChemicalUpdate = stepsPerChemicalUpdate
        self.stepsPerRobotMovement = stepsPerRobotMovement
        self.time = 0
        

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
                else:
                    b = 0.0
                robots[x, y] = Robot(1.0, 0.1 * np.random.random() + b,x + offset,y + offset,self.rdParams)
        self.robots = robots.ravel()
        
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
        self.time += 1
        if self.time % self.stepsPerChemicalUpdate == 0:
            for robot in self.robots:
                self.calcNeighbors(robot)
            for robot in self.robots:
                robot.setDivergence()
                robot.updateChemicals()
        if self.time % self.stepsPerRobotMovement == 0:
            # If there is no moving robot, pick a new one
            if not self.movingRobot:
                dissatisfiedRobots = []
                for edgeRobot in self.edgeRobots:
                    if(edgeRobot.isDissatisfied()):
                        dissatisfiedRobots.append(edgeRobot)
                self.movingRobot = np.random.choice(dissatisfiedRobots,1)[0]

            # Move the robot
            oldNeighbors = self.movingRobot.neighbors.ravel()
            self.grid[self.movingRobot.x][self.movingRobot.y] = 0
            self.movingRobot.move()
            self.grid[self.movingRobot.x][self.movingRobot.y] = self.movingRobot
            self.calcNeighbors(self.movingRobot)
            newNeighbors = self.movingRobot.neighbors.ravel()
 
            allNeighbors = set(oldNeighbors).union(set(newNeighbors))
            # Update isOnEdge attribute of neighbors of moving robot
            for neighbor in allNeighbors:
                if isinstance(neighbor, Robot):
                    self.calcNeighbors(neighbor)
                    onEdge = neighbor.isOnEdge
                    if onEdge:
                        self.edgeRobots.add(neighbor)
                    elif neighbor in self.edgeRobots:
                        self.edgeRobots.remove(neighbor)

            # Check if the robot is satisfied
            if(not self.movingRobot.isDissatisfied()):
                self.movingRobot = None

    def plottableGrid(self, grid):
        vectorized_grid = np.vectorize(lambda x: x.b if isinstance(x, Robot) else -1, otypes=[np.float32])
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
            print(i)
            for _ in range(self.stepsPerFrame):
                self.updateSimulation()
            plotGrid = self.plottableGrid(self.grid)
            mask = plotGrid < 0
            with sns.axes_style("white"):
                sns.heatmap(plotGrid, mask = mask, vmax = 1, cbar=False)
        
        anim = FuncAnimation(fig, updateFrame, init_func=self.initPlot, frames=self.nSteps//self.stepsPerFrame, repeat=False)

        # Writer = writers['imagemagick']
        # writer = Writer(fps=20, metadata=dict(artist='Me'), bitrate=1800)
        # anim.save('0.4_0.2_0.039_-0.104_2000_frames_b.gif', writer=writer)
        plt.show()



if __name__ == '__main__':
    sim = Simulator(nSteps = 400, gridSize=60, rdParams=[0.4,0.2,0.039,-0.104],sideLength=50, stepsPerFrame=1)

    sim.main()
