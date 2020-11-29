import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

class Robot(object):
    """docstring for Robot."""

    def __init__(self,a,b,x,y,rd_params): # neighborRadius
        self.a = a
        self.b = b
        self.ca, self.cb, self.a_add_rate, self.b_add_rate = rd_params
        # self.neighborRadius = neighborRadius
        self.x = x
        self.y = y

    def detectEdge(self):
        "returns true if agent is on edge"
        pass

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

        reaction = self.a * self.b**2
        divA = -self.a * 4 + sum(neighborA)
        divB = -self.b * 4 + sum(neighborB)
        self.a += divA * self.ca - reaction + self.a_add_rate * (1-self.a)
        self.b += divB * self.cb + reaction + self.b_add_rate * self.b

    def getLEDValue(self):
        # finish this when we plot, map from a to col
        return self.a

    def calcMoves(self):
        "returns list of empty squares to move to"

    def move(self):
        "calculates where to move, then moves agent. no return value"
        moves = self.calc_moves()
        pass
