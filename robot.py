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

    def detectEdge(self):
        "returns true if agent is on edge"
        vec_neighbor = np.vectorize(lambda x: 1 if isinstance(x, Robot) else 0, otypes=[np.float32])
        kernel = np.array([[0, -1, 0],
                           [-1, 4, -1],
                           [0, -1, 0]])
        adj_neighbors = vec_neighbor(self.neighbors)
        return (adj_neighbors * kernel).sum() > 0


    def move(self):
        matchKernel = np.array([[0,1,0],
                                [1,-10,1],
                                [0,1,0]])
        vec_neighbor = np.vectorize(lambda x: 1 if isinstance(x, Robot) else 0, otypes=[np.int])
        robot_neighbors = vec_neighbor(self.neighbors)
        robot_neighbors[1][1] = 0
        matchedCells = scipy.signal.correlate2d(robot_neighbors, matchKernel, mode='same')
        matchedCells[(self.lastX-self.x)+1][(self.lastY-self.y)+1] = -1
        matches = np.where(matchedCells > 0)


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
        # later we can scale the diffusion by the distance?
        divA = np.vectorize(lambda x: x.a if isinstance(x, Robot) else 0, otypes=[np.float32])
        divB = np.vectorize(lambda x: x.b if isinstance(x, Robot) else 0, otypes=[np.float32])
        self.divA = (divA(self.neighbors) * self.kernel).sum()
        self.divB = (divB(self.neighbors) * self.kernel).sum()


    def setNeighbors(self,neighbors):
        "sets the internal neighbors"
        self.neighbors = neighbors

    def updateChemicals(self):
        # later we can scale the diffusion by the distance?
        # neighborA = [neighbor.a for neighbor in self.neighbors]
        # neighborB = [neighbor.b for neighbor in self.neighbors]
        # while len(neighborA) < 4:
        #     neighborA.append(0)
        # while len(neighborB) < 4:
        #     neighborB.append(0)

        reaction = self.a * self.b**2
        # divA = -self.a * 4 + sum(neighborA)
        # divB = -self.b * 4 + sum(neighborB)
        self.a += self.divA * self.ca - reaction + self.a_add_rate * (1-self.a)
        self.b += self.divB * self.cb + reaction + self.b_add_rate * self.b

    def getLEDValue(self):
        # finish this when we plot, map from a to col
        return self.a

    def calcMoves(self):
        "returns list of empty squares to move to"

    def move(self):
        "calculates where to move, then moves agent. no return value"
        moves = self.calc_moves()
        pass
