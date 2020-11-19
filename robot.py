import numpy as np
import matplotlib.pyplot as plt
import scipy.signal


class Robot(object):
    """docstring for Robot."""

    def __init__(self,a,b,x,y,neighbor_radius,rd_params):
        self.a = a
        self.b = b
        self.rd_params = rd_params
        self.neighbor_radius = neighbor_radius
        self.pos = np.array([[x, y]])

    def detect_edge(self):
        "returns true if agent is on edge"
        pass

    def set_neighbors(self,neighbors):
        "sets the internal neighbors"
        self.neighbors = neighbors

    def calc_moves(self):
        "returns list of empty squares to move to"

    def move(self):
        "calculates where to move, then moves agent. no return value"
        moves = self.calc_moves()
        pass
