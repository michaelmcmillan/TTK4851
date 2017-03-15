import math
import controller
import robot
import time

# Create flags for decisions
waypoint_flag = False
THREASHOLD_POS = 2
THREASHOLD_ANG_MAX = 15
THREASHOLD_ANG_MIN = 5
THREASHOLD_COORDINATES = 5
SAMPLE_TIME = 0.1
ROBOT_LENGHT = 13


# Create Controllers
posistion_controller = controller.PID(5.5, 2, 1.5)
posistion_controller.setSampleTime(SAMPLE_TIME)
posistion_controller.setSetpoint(0)

angle_controller = controller.PID(1, 10, 0)
angle_controller.setSampleTime(SAMPLE_TIME)

ang_ctrl_output = 0
pos_ctrl_output = 0

# 1D Variables for angle and distance
dist_ref = 0.0
dist_robot = 0.0
ang_ref = 0.0
ang_robot = 0.0

xref = 0.0
yref = 0.0

# Get the refrence angle value from coordinates
def get_ang_ref(xpos_ref, ypos_ref, xpos_robot, ypos_robot):
    adj = xpos_ref - xpos_robot
    opp = ypos_ref - ypos_robot
    ang_ref = math.degrees(math.atan2(opp, adj))
    return ang_ref

def ang_offset(ang_rob, ang_ref):
    #TODO: lag logic for aa skjekke vinkel differense
    aoff = math.fabs(ang_rob) - math.fabs(ang_ref)
    return aoff

# Get distance from robot to waypoint in 1D
def get_dist_robot(xpos_ref, ypos_ref, xpos_robot, ypos_robot):
    # Find distance from robot to waypoint

    if math.fabs(xpos_ref - xpos_robot) < THREASHOLD_COORDINATES:
        dist = math.fabs(ypos_ref - ypos_robot)

    elif math.fabs(ypos_ref - ypos_robot) < THREASHOLD_COORDINATES:
        dist = math.fabs(xpos_ref - xpos_robot)
    else:
        adj = xpos_ref - xpos_robot
        opp = ypos_ref - ypos_robot
        dist = math.sqrt(math.pow(adj, 2) + math.pow(opp, 2))

    # Testing with utrasonic as distance measurement
    dist_robot = robot.read_ultrasonic()

    return dist_robot


def controlloop(xrob, yrob, waypoints):
    global waypoint_flag

    # Remove last waypoint from list
    if waypoint_flag:
        waypoints.pop(0)
        waypoints.pop(0)
        waypoint_flag = False

    # Extract correct waypoint
    xref = waypoints[0]
    yref = waypoints[1]

    # Get robot/ref distance and angle
    dist_rob = get_dist_robot(xref, yref, xrob, yrob)
    ang_rob = robot.read_compass()                                          # From Compass
    ang_ref = get_ang_ref(xref, yref, xrob, yrob)                                                 # Calculated from coordinates
    ang_off = ang_offset(ang_rob, ang_ref)                     # Offset in angle

    # Angle offset logic
    off_cource_flag = True
    if math.fabs(ang_off) > THREASHOLD_ANG_MAX:
        off_cource_flag = True
    if math.fabs(ang_off) < THREASHOLD_ANG_MIN:  # Check offset
        off_cource_flag = False

    # Angle controller
    if off_cource_flag:
        posistion_controller.clear()                                        # Reset posistion controller
        pos_ctrl_output = 0
        angle_controller.setSetpoint(ang_ref)                               # Set setpoint for angle
        ang_ctrl_output = angle_controller.update(ang_rob)                  # Update controller
        print("DISTANCE: " + str(dist_rob) + "\tCOMPASS: " + str(ang_rob) + "\tANGLE OFFSET: " + str(
            ang_off) + "\tPOSISTION_OUTPUT " + str(pos_ctrl_output) + "\t\t\tANGLE OUTPUT: " + str(ang_ctrl_output))

        output = [pos_ctrl_output, ang_ctrl_output]
        return output
        #robot.turn(SAMPLE_TIME, int(ang_ctrl_output))


    # Posistion controller
    else:
        angle_controller.clear()                                             # Reset angle controller
        ang_ctrl_output = 0
        pos_ctrl_output = posistion_controller.update(dist_rob)
        # TODO: Return ang_ctrl_output and pos_ctrl_otput
        print("DISTANCE: " + str(dist_rob) + "\tCOMPASS: " + str(ang_rob) + "\tANGLE OFFSET: " + str(
            ang_off) + "\tPOSISTION_OUTPUT " + str(pos_ctrl_output) + "\t\t\tANGLE OUTPUT: " + str(ang_ctrl_output))

        output = [pos_ctrl_output, ang_ctrl_output]
        return output
        #robot.walk(SAMPLE_TIME, int(pos_ctrl_output))

    # Check if waypoint is reached
    if dist_rob < THREASHOLD_POS:                                           #check if robot has reached the waypoint
        waypoint_flag = True


    time.sleep(1)


# TEST
L = [10.0, 0.0, 10.0, 10.0];
while True:
    output = controlloop(0.0,0.0,L)
    robot.walk(SAMPLE_TIME, int(output[0]))
    robot.turn(SAMPLE_TIME, int(output[1]))