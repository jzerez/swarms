import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import random
import copy
class Robot(object):
    """
    Robot class keeps track of all the chemical values for an individual and processes the movement.
    """
    def __init__(self,a,b,x,y,rd_params):
        """
        Initializes the robot class
        Arguments:
            a (float): initial chemical of a concentration
            b (float): initial b concentration
            x (int): initial x position
            y (int): initial y position
            rd_params (list(float)): parameters for the robot diffusion
        """
        self.a = a
        self.b = b
        self.ca, self.cb, self.a_add_rate, self.b_add_rate = rd_params
        self.x = x
        self.y = y
        self.divA = 0
        self.divB = 0
        self.lastX = x
        self.lastY = y
        # Kernel for calculating divergence of chemicals
        self.kernel = np.array([[.05, .2, .05],
                                [ .2, -1, .2],
                                [.05, .2, .05]])
                                
        # Kernel for calculating valid moves for a robot
        self.matchKernel = np.array([[0,1,0],
                                     [1,-10,1],
                                     [0,1,0]])

        # Kernel for detecting if an robot is on the edge
        # A robot is on the edge if it has 5 or fewer robot neighbors 
        self.edgeKernel = np.array([[-1, -1,-1],
                                    [-1, 6, -1],
                                    [-1, -1,-1]])

        # Bool to keep track of if the robot is on the edge or not
        self.isOnEdge = False
        # Bool to keep track of if the robot is dead or not
        # A robot is dead if it has no robot neighbors
        self.isDead = False

    def getRobotNeighbors(self, attr=None, dtype=np.int):
        """
        Returns a list of the neighbors that are robots, optionally with an attribute of them
        Arguments:
            attr (dtype type): attribute of the robot to return
            dtype (type): type of attr
        Returns:
            np.array(dtype) A vector of either the robots or the attribute of the robots specified
        """

        if attr is None:
            vec = np.vectorize(lambda x: 1 if isinstance(x, Robot) else 0, otypes=[dtype])
        else:
            vec = np.vectorize(lambda x: getattr(x, attr) if isinstance(x, Robot) else 0, otypes=[dtype])

        return vec(self.neighbors)

    def detectEdge(self):
        """
        Calculates whether the robots is on an edge, or completely isolated
        Returns:
            (bool) if robot is on edge or completely isolated
        """
        adj_neighbors = self.getRobotNeighbors()
        edgeSum = (adj_neighbors * self.edgeKernel).sum()
        if edgeSum!= 6:
            self.isDead = False
            return edgeSum > 0
        else:
            self.isDead = True
            return False

        
    def isSatisfied(self):
        """
        calculates whether the robot is satisfied (defined as being close to a robot with sufficient concentration of a chemical)
        Returns:
            (bool) is the robot satisfied
        """
        for neighbor in self.neighbors.ravel():
            if(neighbor != 0):
                if(neighbor.b >= 0.05):
                    return True
        return False


    def move(self):
        """
        Moves the robot one space along the edge, not going back to a space it just came from.
        Returns:
            (int,int) new position of the robot
        """
        robot_neighbors = self.getRobotNeighbors()
        robot_neighbors[1][1] = 0
        # matched cells is a 3x3 where positive numbers are valid moves
        matchedCells = scipy.signal.correlate2d(robot_neighbors, self.matchKernel, mode='same')
        # current position is invalid (impossible to not move)
        matchedCells[1][1] = -1

        if (matchedCells > 0).sum() > 1:
            # previous position is invalid and there are no other spots
            matchedCells[(self.lastX-self.x)+1][(self.lastY-self.y)+1] = -1
        
        matches = np.where(matchedCells > 0)
        # Robot became an orphan, all of its neighbors left :(
        if len(matches[0]) - 1 < 0:
            self.isDead = True
            return(self.x, self.y)

        index = random.randint(0,len(matches[0])-1)
        self.lastX = self.x
        self.lastY = self.y
        self.x = self.x+matches[0][index]-1
        self.y = self.y+matches[1][index]-1
        return (self.x,self.y)

    def setNeighbors(self,neighbors):
        """
        Sets the robot's list of neighbors to be the incoming list of neigbors
        Arguments:
            neighbors (np.array(Robot or int))): 
        """
        self.neighbors = neighbors

    def setDivergence(self):
        """
        Sets the divergence in each chemical according to the neighbor's concentrations.
        """
        self.divA = 0
        self.divB = 0

        for kernelVal, neighbor in zip(self.kernel.flat, self.neighbors.flat):
            if neighbor != 0:
                self.divA += neighbor.a * kernelVal
                self.divB += neighbor.b * kernelVal
            else:
                # If there is no robot, pretend that the value is the same as the current grid space
                # This effectively prevents chemicals from diffusing out 
                self.divA += self.a * kernelVal
                self.divB += self.b * kernelVal

    def updateChemicals(self):
        """
        Sets the new chemical concentrations based no the divergence and reaction
        """
        reaction = self.a * self.b**2

        self.a += self.divA * self.ca - reaction + self.a_add_rate * (1-self.a)
        self.b += self.divB * self.cb + reaction + self.b_add_rate * self.b