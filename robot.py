import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import random

class Robot(object):
    """docstring for Robot."""

    def __init__(self,a,b,x,y,rd_params): # neighborRadius
        self.a = a
        self.b = b
        self.ca, self.cb, self.a_add_rate, self.b_add_rate = rd_params
        # self.neighborRadius = neighborRadius
        self.x = x
        self.y = y
        self.divA = 0
        self.divB = 0
        self.lastX = x
        self.lastY = y
        self.kernel = np.array([[.05, .2, .05],
                                [ .2, -1, .2],
                                [.05, .2, .05]])
        self.isOnEdge = False

    def getRobotNeighbors(self, attr=None, dtype=np.int):
        if attr is None:
            vec = np.vectorize(lambda x: 1 if isinstance(x, Robot) else 0, otypes=[dtype])
        else:
            vec = np.vectorize(lambda x: getattr(x, attr) if isinstance(x, Robot) else 0, otypes=[dtype])

        return vec(self.neighbors)

    def detectEdge(self):
        "returns true if agent is on edge"
        adj_neighbors = self.getRobotNeighbors()
        kernel = np.array([[0, -1, 0],
                           [-1, 4, -1],
                           [0, -1, 0]])
        return (adj_neighbors * kernel).sum() > 0
        
    def isDissatisfied(self):
        for neighbor in self.neighbors.ravel():
            if(neighbor != 0):
                if(neighbor.b >= 0.2):
                    return False
        return True


    def move(self):
        matchKernel = np.array([[0,1,0],
                                [1,-10,1],
                                [0,1,0]])
        robot_neighbors = self.getRobotNeighbors()
        robot_neighbors[1][1] = 0
        matchedCells = scipy.signal.correlate2d(robot_neighbors, matchKernel, mode='same')
        matchedCells[(self.lastX-self.x)+1][(self.lastY-self.y)+1] = -1
        matchedCells[1][1] = -1
        matches = np.where(matchedCells > 0)
        for i in range(len(matches[0])):
            print("(",matches[0][i],matches[1][i],end=") , ")


        index = random.randint(0,len(matches[0])-1)
        self.lastX = self.x
        self.lastY = self.y
        self.x = self.x+matches[0][index]-1
        self.y = self.y+matches[1][index]-1
        return (self.x,self.y)

    def setNeighbors(self,neighbors):
        "sets the internal neighbors"
        self.neighbors = neighbors

    def setDivergence(self):
        neighborA = self.getRobotNeighbors('a', np.float32)
        neighborB = self.getRobotNeighbors('b', np.float32)

        self.divA = (neighborA * self.kernel).sum()
        self.divB = (neighborB * self.kernel).sum()


    def updateChemicals(self):
        reaction = self.a * self.b**2

        self.a += self.divA * self.ca - reaction + self.a_add_rate * (1-self.a)
        self.b += self.divB * self.cb + reaction + self.b_add_rate * self.b
    
    def getLEDValue(self):
        # finish this when we plot, map from a to col
        return self.a

    def calcMoves(self):
        "returns list of empty squares to move to"
        pass
