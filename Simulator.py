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
    """
    Simulator object. Responsible for simulating the local interactions of the robots and for updating the grid world
    """

    def __init__(self, nSteps, gridSize, rdParams, sideLength, stepsPerFrame=25, stepsPerChemicalUpdate=1, stepsPerRobotMovement=2):
        """
        Initialization Function for Simulator object

        Arguments:
            nSteps     (int):   The number of timesteps to solve for in the simulation
            gridSize (tuple):   A tuple of ints describing the size of the grid to use (x,y)
            rdParams (tuple):   A tuple of floats containing reaction-diffusion constants
            sideLength (int):   The number of robots in the diameter of the initial clump of robots
            stepsPerFrame (int): The number of timesteps between each frame rendered in the animation
            stepsPerChemicalUpdate (int): The number of timesteps between each chemical update
            stepsPerRobotMovement (int):  The number of timesteps between each robot movement
        
        Returns:
            None
        """
        self.rdParams = rdParams
        self.nSteps = nSteps
        self.gridSize = gridSize
        self.sideLength = sideLength

        # Create the file name for the animation rendered
        self.file_name = ""
        for rdParam in rdParams:
            self.file_name += str(rdParam) + "_"
        self.file_name += str(nSteps)+"frames.gif"

        self.movingRobot = None
        self.robots = []
        # initialize the grid with robots and with empty spaces. 
        self.grid = self.initGrid()

        # Initialize robots with their neighbor robots
        for robot in self.robots:
            self.calcNeighbors(robot)
        # Find and store robots on the edge of the swarm
        # Use a set because we want to check membership in O(1) time
        self.edgeRobots = set([robot for robot in self.robots if robot.detectEdge()])

        self.stepsPerFrame = stepsPerFrame
        self.stepsPerChemicalUpdate = stepsPerChemicalUpdate
        self.stepsPerRobotMovement = stepsPerRobotMovement
        self.time = 0
        

    def initGrid(self):
        """
        Initializes the grid for the simulation and the robots within the grid

        Returns:
            grid (np.array(objects)): An np object array that contains the robots and empty spaces
        """
        offset = (self.gridSize - self.sideLength) // 2
        robots = np.zeros((self.sideLength, self.sideLength), dtype=np.object)

        def inCenter(coor, r=8):
            """
            Determines whether a robot is in the center of the swarm or not
            Arguments:
                coor (int): an x or y coordinate
                r    (int): the threshold distance for something considered to be in the "center"
            Returns
                    (bool): Whether the coordinate is in the center or not 
            """
            return abs(coor - self.sideLength / 2) < self.sideLength / r

        # Populates initial circle of robots. 
        # Robots in the center start with a bit of extra of chemical B to start reaction
        # Saves robots to self.robots list
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
        
        # Creates the grid, and places the circle of robots within the center of the grid
        grid = np.zeros((self.gridSize, self.gridSize), dtype=object)
        firstInd = offset
        secondInd = firstInd + self.sideLength
        grid[firstInd:secondInd, firstInd:secondInd] = robots
        return grid

    def calcNeighbors(self, robot):
        """
        Finds the visible neighbors of a robot. No return value
        Arguments:
            robot (Robot): The robot to calculate the neighbors for
        """

        # Use array indexing to find the (3x3) grid of elements around the current robot
        neighbors = copy.copy(self.grid[robot.x-1:robot.x+2, robot.y-1:robot.y+2])
        
        # Check to make sure that the center grid space of the (3x3) is actually a robot
        # (It should be, because the center should always be equal to the `robot` argument provided)
        if neighbors[1][1] == 0:
            print('uhoh')

        robot.setNeighbors(neighbors)
    
    # Profiling tag. Used for determining runtime. 
    # @profile
    def updateSimulation(self):
        """
        Updates the simulation, handling movement and chemical updates
        """

        # increment timestep
        self.time += 1
        if self.time % self.stepsPerChemicalUpdate == 0:
            self.processChemicals()
        if self.time % self.stepsPerRobotMovement == 0:
            # Have agents move 4 times per "movement" event
            for i in range(4):
                self.processMovement()
    
    # @profile
    def processChemicals(self):
        """
        Updates the chemicals of the robots
        """
        for robot in self.robots:
            robot.setDivergence()
            robot.updateChemicals()
                
    def processMovement(self):
        """
        Moves a robot, and updates surrounding robots
        """
        # If there is no moving robot, pick a new one
        if not self.movingRobot:
            self.pickNewMovingRobot() 
        
        # Move the robot, and find the neighbors of the robot in the new position
        changedNeighbors = self.moveRobot()
        # For each robot in the new neighbors, update whether they are on the edge of the swarm or not              
        self.updateOnEdge(changedNeighbors)          
        # Check if the robot is satisfied and alive
        if(self.movingRobot.isSatisfied() or self.movingRobot.isDead):
            self.movingRobot = None

    def pickNewMovingRobot(self):
        """
        Picks a new robot to move, from the robots that are on the edge and dissatisfied
        """         
        dissatisfiedRobots = []
        for edgeRobot in self.edgeRobots:
            if not edgeRobot.isSatisfied() and not edgeRobot.isDead:
                dissatisfiedRobots.append(edgeRobot)
        self.movingRobot = np.random.choice(dissatisfiedRobots,1)[0]

    def moveRobot(self):
        """
        Moves the robot to a new grid space based on it's edge following
        Returns:
            set(Robot): The neighbors that were affected by the robot's move
        """
        # Store the neighbors of the robot in the current position
        oldNeighbors = self.movingRobot.neighbors.flatten()
        # Replace the current position of the robot with an empty cell
        self.grid[self.movingRobot.x][self.movingRobot.y] = 0
        self.movingRobot.move()
        # Update grid with new position of robot
        self.grid[self.movingRobot.x][self.movingRobot.y] = self.movingRobot
        self.calcNeighbors(self.movingRobot)
        newNeighbors = self.movingRobot.neighbors.flatten()

        return set(oldNeighbors).union(set(newNeighbors))

    def updateOnEdge(self,changedNeighbors):
        """
        Takes the set of changed neighbors and updates their edge status
        Arguments:
            changedNeighbors (set(Robot)): the neighbors that were affected by the robot's last move
        """
        for neighbor in changedNeighbors:
            if isinstance(neighbor, Robot):
                self.calcNeighbors(neighbor)
                onEdge = neighbor.detectEdge()
                if onEdge:
                    self.edgeRobots.add(neighbor)
                elif neighbor in self.edgeRobots:
                    self.edgeRobots.remove(neighbor)
                
                    
    def plottableGrid(self, grid):
        """
        Takes the grid of robots and converts each one to be the b concentration of that robot
        Arguments:
           grid (np.array(Objects)) - either Robot or 0
        Returns:
            list(list(int))
        """
        def filter(x):
            if isinstance(x, Robot):
                return x.b
                # if x in self.edgeRobots:
                #     return 1
                # else:
                #     return x.b
            else:
                return -1
        vectorized_grid = np.vectorize(lambda x: filter(x), otypes=[np.float32])
        return vectorized_grid(grid)


    def initPlot(self):
        """
        Initializes the plotted grid
        """
        plotGrid = self.plottableGrid(self.grid)
        # mask out non-robot grid spaces
        maskedGrid = np.ma.masked_where(plotGrid < 0, plotGrid)
        plottedGrid = self.ax.imshow(maskedGrid, vmin=0, vmax=1)
        self.fig.colorbar(plottedGrid)


    def main(self):
        """
        Runs the simulation
        """
        self.fig, self.ax  = plt.subplots()

        def updateFrame(i):
            print(i)
            for _ in range(self.stepsPerFrame):
                self.updateSimulation()
            plotGrid = self.plottableGrid(self.grid)
            maskedGrid = np.ma.masked_where(plotGrid < 0, plotGrid)
            self.ax.cla()
            self.ax.imshow(maskedGrid, vmin=0, vmax=1)
        
        anim = FuncAnimation(self.fig, updateFrame, init_func=self.initPlot, frames=self.nSteps//self.stepsPerFrame, repeat=False)

        Writer = writers['imagemagick']
        writer = Writer(fps=45, metadata=dict(artist='Me'), bitrate=1800)
        anim.save(self.file_name, writer=writer)
        # # anim.save('delete_me.gif', writer=writer)
        # plt.show()



if __name__ == '__main__':
    sim = Simulator(nSteps = 10100, gridSize=75, rdParams=(0.43,0.19,0.035,-0.100),sideLength=35, stepsPerFrame=50, stepsPerChemicalUpdate=1)
    sim.main()
