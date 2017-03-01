import math
from unittest import TestCase, skip
from src.control_system.brick_class import Walker

class PidVariables:

    def __init__(self):

        # 1D
        self.dist_ref = 0
        self.dist_robot = 0
        self.ang_ref = 0
        self.ang_robot = 0


        # 2D
        self.xpos_robot = 0
        self.ypos_robot = 0
        self.xpos_ref = 0
        self.ypos_ref = 0

        walker = Walker()

    def set_new_waypoint(self):                                                 # should alter the waypoint for the posiston
        # TODO: new xref and yref from matrix
        self.xpos_ref = 0
        self.ypos_ref = 0
        pass

    def get_ang_ref(self):

        adj = self.xpos_ref - self.xpos_robot                                   # Update varibles before use
        opp = self.ypos_ref - self.ypos_robot
        self.ang_ref = math.degrees(math.atan2(opp, adj))
        return self.ang_ref

    def get_ang_robot(self):
        self.ang_robot = 0
        self.ang_robot = self.walker.compass()
        return self.ang_robot

    # Shift 1D coordinate system
    def get_dist_robot(self):
        # Find distance from robot to waypoint
        adj = self.xpos_ref - self.xpos_robot
        opp = self.ypos_ref - self.ypos_robot

        #In 1D: waypoint = 0, robot = distance to waypoint(origo)
        self.dist_robot = math.sqrt(math.pow(adj, 2) + math.pow(opp, 2))

        return self.dist_robot

    # Maybe not needed??
    def update_coordinates(self):
        # TODO: get robot pos from matrix
        self.xpos_robot = 0  # get value from image
        self.ypos_robot = 0  # get value from image
        self.xpos_ref = 0
        self.ypos_ref = 0












