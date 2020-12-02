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
        self.lastX = None
        self.lastY = None

    def detectEdge(self):
        "returns true if agent is on edge"
        pass

    def move(self):
        matchedCells = np.zeros((3,3))
        circleGrid =       [(0,0),
                            (0,1),
                            (0,2),
                            (1,2),
                            (2,2),
                            (2,1),
                            (2,0),
                            (1,0)]
        for i in range(8):
            if(isinstance(self.gridAround[circleGrid[i][0]][circleGrid[i][1]],Robot)):
                if(i == 0):
                    matchedCells[circleGrid[7][0]][circleGrid[7][1]] = 1
                else:
                    matchedCells[circleGrid[i-1][0]][circleGrid[i-1][1]] = 1
                if(i == 7):
                    matchedCells[circleGrid[0][0]][circleGrid[0][1]] = 1
                else:
                    matchedCells[circleGrid[i+1][0]][circleGrid[i+1][1]] = 1
        matchedCells[(self.lastX-self.x)+1][(self.lastY-self.y)+1] = 0
        matches = np.nonzero(matchedCells)
        index = random.randint(0,len(matches)-1)
        self.lastX = self.x
        self.lastY = self.y
        self.x = self.x+matches[0][index]-1
        self.y = self.y+matches[1][index]-1
        return (self.x,self.y)

    def setGridAround(self,gridAround):
        "I want this to be a 3x3 around the robot"
        self.gridAround = gridAround

    def setNeighbors(self,neighbors):
        "sets the internal neighbors"
        self.neighbors = neighbors

    def updateChemicals(self):
        # later we can scale the diffusion by the distance?
        neighborA = [neighbor.a for neighbor in self.neighbors]
        neighborB = [neighbor.b for neighbor in self.neighbors]
        while len(neighborA) < 4:
            neighborA.append(0)
        while len(neighborB) < 4:
            neighborB.append(0)
        self.divA = -self.a * 4 + sum(neighborA)
        self.divB = -self.b * 4 + sum(neighborB)

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
