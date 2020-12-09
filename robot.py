import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import random
import copy
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
        self.matchKernel = np.array([[0,1,0],
                                     [1,-10,1],
                                     [0,1,0]])
        self.edgeKernel = np.array([[0, -1, 0],
                                    [-1, 4, -1],
                                    [0, -1, 0]])
        self.isOnEdge = False

    def getRobotNeighbors(self, attr=None, dtype=np.int):
        # res = []
        # for elem in self.neighbors.flat:
        #     if elem == 0:
        #         res.append(0)
        #     else:
        #         res.append(1)
        # return np.array(res).reshape((3,3))

        if attr is None:
            vec = np.vectorize(lambda x: 1 if isinstance(x, Robot) else 0, otypes=[dtype])
        else:
            vec = np.vectorize(lambda x: getattr(x, attr) if isinstance(x, Robot) else 0, otypes=[dtype])

        return vec(self.neighbors)

    def detectEdge(self):
        "returns true if agent is on edge"
        adj_neighbors = self.getRobotNeighbors()
        return (adj_neighbors * self.edgeKernel).sum() > 0
        
    def isSatisfied(self):
        for neighbor in self.neighbors.ravel():
            if(neighbor != 0):
                if(neighbor.b >= 0.06):
                    return True
        return False


    def move(self):
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
        if len(matches[0]) - 1 < 0:
            print('uhoh')
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
        reaction = self.a * self.b**2

        self.a += self.divA * self.ca - reaction + self.a_add_rate * (1-self.a)
        self.b += self.divB * self.cb + reaction + self.b_add_rate * self.b
    
    def getLEDValue(self):
        # finish this when we plot, map from a to col
        return self.a