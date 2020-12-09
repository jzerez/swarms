import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import seaborn as sns
import scipy.signal
import rd
from robot import Robot
import time
import copy
from matplotlib.animation import FuncAnimation, writers

class Simulator(object):
    """docstring for Simulator."""

    def __init__(self, nSteps, gridSize, rdParams, sideLength, shape="circle", stepsPerFrame=25, stepsPerChemicalUpdate=1, stepsPerRobotMovement=2):
        # self.a, self.b = rd.reaction_diffusion(n_steps, grid_size, rd_params)
        self.rdParams = rdParams
        self.nSteps = nSteps
        self.gridSize = gridSize
        self.sideLength = sideLength
        self.file_name = ""
        for rdParam in rdParams:
            self.file_name += str(rdParam) + "_"
        self.file_name += str(nSteps)+"frames.gif"

        self.movingRobot = None
        self.robots = []
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

        def inCenter(coor, r=8):
            return abs(coor - self.sideLength / 2) < self.sideLength / r

        for x in range(self.sideLength):
            for y in range(self.sideLength):
                if inCenter(x) and inCenter(y):
                    b = 0.1
                else:
                    b = 0.0
                if((x-self.sideLength/2)**2 + (y-self.sideLength/2)**2 < (self.sideLength/2)**2):
                    nextRobot = Robot(1.0, 0.1 * np.random.random() + b,x + offset,y + offset,self.rdParams)
                    robots[x, y] = nextRobot
                    self.robots.append(nextRobot)
        # self.robots = robots.ravel()
        
        grid = np.zeros((self.gridSize, self.gridSize), dtype=object)
        firstInd = offset
        secondInd = firstInd + self.sideLength
        grid[firstInd:secondInd, firstInd:secondInd] = robots
        return grid

    def calcNeighbors(self, robot):
        "finds the visible neighbors of a robot. No return value"
        neighbors = copy.copy(self.grid[robot.x-1:robot.x+2, robot.y-1:robot.y+2])
        if neighbors[1][1] == 0:
            print('uhoh')
        # TODO: if the middle element is a zero, then set breakpoint
        robot.setNeighbors(neighbors)
    
    # @profile
    def updateSimulation(self):
        self.time += 1
        if self.time % self.stepsPerChemicalUpdate == 0:
            self.processChemicals()
        if self.time % self.stepsPerRobotMovement == 0:
            for i in range(4):
                self.processMovement()
    
    # @profile
    def processChemicals(self):
        for robot in self.robots:
            robot.setDivergence()
            robot.updateChemicals()
                
    def processMovement(self):
        # If there is no moving robot, pick a new one
        if not self.movingRobot:
            self.pickNewMovingRobot() 
        changedNeighbors = self.moveRobot()              
        self.updateOnEdge(changedNeighbors)          
        # Check if the robot is satisfied
        if(self.movingRobot.isSatisfied()):
            self.movingRobot = None

    def pickNewMovingRobot(self):         
        dissatisfiedRobots = []
        for edgeRobot in self.edgeRobots:
            if(not edgeRobot.isSatisfied()):
                dissatisfiedRobots.append(edgeRobot)
        self.movingRobot = np.random.choice(dissatisfiedRobots,1)[0]

    def moveRobot(self):
        # Move the robot
        oldNeighbors = self.movingRobot.neighbors.flatten()
        self.grid[self.movingRobot.x][self.movingRobot.y] = 0
        self.movingRobot.move()
        self.grid[self.movingRobot.x][self.movingRobot.y] = self.movingRobot
        self.calcNeighbors(self.movingRobot)
        newNeighbors = self.movingRobot.neighbors.flatten()

        return set(oldNeighbors).union(set(newNeighbors))

    def updateOnEdge(self,changedNeighbors):
        # Update isOnEdge attribute of neighbors of moving robot
        for neighbor in changedNeighbors:
            if isinstance(neighbor, Robot):
                self.calcNeighbors(neighbor)
                onEdge = neighbor.detectEdge()
                if onEdge:
                    self.edgeRobots.add(neighbor)
                elif neighbor in self.edgeRobots:
                    self.edgeRobots.remove(neighbor)
    def plottableGrid(self, grid):
        vectorized_grid = np.vectorize(lambda x: x.b if isinstance(x, Robot) else -1, otypes=[np.float32])
        return vectorized_grid(grid)


    def initPlot(self):
        plotGrid = self.plottableGrid(self.grid)
        maskedGrid = np.ma.masked_where(plotGrid < 0, plotGrid)
        plottedGrid = self.ax.imshow(maskedGrid, vmin=0, vmax=1)
        self.fig.colorbar(plottedGrid)
        # with sns.axes_style("white"):
        #     self.ax = sns.heatmap(plotGrid, mask = mask, vmax = 1, vmin=0)


    def main(self):
        self.fig, self.ax  = plt.subplots()

        def updateFrame(i):
            print(i)
            for _ in range(self.stepsPerFrame):
                self.updateSimulation()
            plotGrid = self.plottableGrid(self.grid)
            mask = plotGrid < 0
            maskedGrid = np.ma.masked_where(plotGrid < 0, plotGrid)
            self.ax.cla()
            self.ax.imshow(maskedGrid, vmin=0, vmax=1)
        
        anim = FuncAnimation(self.fig, updateFrame, init_func=self.initPlot, frames=self.nSteps//self.stepsPerFrame, repeat=False)

        Writer = writers['imagemagick']
        writer = Writer(fps=45, metadata=dict(artist='Me'), bitrate=1800)
        anim.save(self.file_name, writer=writer)
        # anim.save('delete_me.gif', writer=writer)
        # plt.show()



if __name__ == '__main__':
    sim = Simulator(nSteps = 80000, gridSize=75, rdParams=(0.5,0.25,0.06,-0.124),sideLength=35, stepsPerFrame=100)

    sim.main()
