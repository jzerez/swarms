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
        self.pos = np.array([[x, y]])

    def detectEdge(self):
        "returns true if agent is on edge"
        pass

    def setNeighbors(self,neighbors):
        "sets the internal neighbors"
        self.neighbors = neighbors

    def updateChemicals(self):
        # later we can scale the diffusion by the distance?
        neighborMeanA = np.mean([neighbor.a for neighbor in self.neighbors])
        neighborMeanB = np.mean([neighbor.b for neighbor in self.neighbors])
        reaction = a * b**2
        self.a += (-self.a + neighborMeanA) * self.ca - reaction + self.a_add_rate * (1-a)
        self.b += (-self.b + neighborMeanB) * self.cb + reaction + self.b_add_rate * b

    def getLEDValue(self):
        # finish this when we plot, map from a to col
        return self.a

    def calcMoves(self):
        "returns list of empty squares to move to"

    def move(self):
        "calculates where to move, then moves agent. no return value"
        moves = self.calc_moves()
        pass
