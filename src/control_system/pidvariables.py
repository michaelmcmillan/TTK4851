import math

class PidVariables:

    def __init__(self, tolerated_ang_offset):

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


        self.ref = 0
        self.robot = 0

        self.tolerated_ang_offset = tolerated_ang_offset

    def set_new_waypoint(self):
        #new xref and yref
        pass

    def set_ang_ref(self):
        adj = self.xpos_ref - self.xpos_robot                                   # Update varibles before use
        opp = self.ypos_ref - self.ypos_robot
        self.ang_ref = math.degrees(math.atan2(opp, adj))

    def get_ang_robot(self):
        self.ang_robot = 0                                                      # get value from compass
        return self.ang_robot

    # Shift 1D coordinate system
    def get_dist_robot(self):
        # Get 2D coordinates
        self.xpos_robot = 0                                                     # get value from image
        self.ypos_robot = 0                                                     # get value from image
        self.xpos_ref = 0
        self.ypos_ref = 0

        # Find distance from robot to waypoint
        adj = self.xpos_ref - self.xpos_robot
        opp = self.ypos_ref - self.ypos_robot

        #In 1D: waypoint = 0, robot = distance to waypoint(origo)
        self.dist_robot = math.sqrt(math.pow(adj, 2) + math.pow(opp, 2))

        return self.dist_robot

    #
    def get_pos_robot(self):
        self.xpos_robot = 0                                                     # get value from image
        self.ypos_robot = 0                                                     # get value from image














