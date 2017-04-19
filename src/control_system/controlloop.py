import math
import controller
import robot

# Create flags for decisions
waypoint_flag = False
THREASHOLD_ANG_MAX = 10 #10
THREASHOLD_ANG_MIN = 5
THREASHOLD_COORDINATES = 5
SAMPLE_TIME = 0.1
ROBOT_LENGHT = 13
SCALE_FACTOR = 5
turning_flag = False
priv_turn = 0
priv_forward = 0


ANGLE_CALIBRATION=30


# Create Controllers
posistion_controller = controller.PID(5, 5, 0)
posistion_controller.setSampleTime(SAMPLE_TIME)
posistion_controller.setSetpoint(0)

# These constants are determined by looking at the robot
# when the battery is fully charged
#angle_controller = controller.PID(0.01, 5, 0)
angle_controller = controller.PID(0.5, 0, 1)
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

# Get distance from robot to waypoint in 1D
def get_dist_robot(xpos_ref, ypos_ref, xpos_robot, ypos_robot):
    # Find distance from robot to waypoint
    if math.fabs(xpos_ref - xpos_robot) == 0:
        dist = math.fabs(ypos_ref - ypos_robot)

    elif math.fabs(ypos_ref - ypos_robot) == 0:
        dist = math.fabs(xpos_ref - xpos_robot)
    else:
        adj = xpos_ref - xpos_robot
        opp = ypos_ref - ypos_robot
        dist = math.sqrt(math.pow(adj, 2) + math.pow(opp, 2))

    # Testing with utrasonic as distance measurement
    dist_robot = robot.read_ultrasonic() - 10

    # Only use coordinates to determine if motor should be on/off
    return dist #dist_robot


# Correct the compass angle
def ang_robot():
    ang = robot.read_compass() - ANGLE_CALIBRATION
    if ang > 180:
        return ang-360
    else:
        return ang

# Update off_cource_flag used to decide what to controll
def offset(ang_rob, ang_ref):
    global off_cource_flag
    ang_off = math.fabs(ang_ref)- math.fabs(ang_rob)

    off_cource_flag = True
    if math.fabs(ang_off) > THREASHOLD_ANG_MAX:
        off_cource_flag = True
    else:
	off_cource_flag = False
    #if math.fabs(ang_off) < THREASHOLD_ANG_MIN:
    #    off_cource_flag = False


def controlloop(robot_coordinate, ref):
    global off_corce_flag
    global priv_forward
    global priv_turn
    global pos_ctrl_output
    global ang_ctrl_output

    # Extract coordinates
    xrob = robot_coordinate[0]
    yrob = robot_coordinate[1]

    xref = ref[0][0]
    yref = ref[0][1]

    # Get robot/ref distance and angle
    dist_rob = get_dist_robot(xref, yref, xrob, yrob)
    ang_rob = ang_robot()                                                                       # From Compass
    ang_ref = get_ang_ref(xref, yref, xrob, yrob)                                               # Calculated from coordinates


    # Angle offset logic
    offset(ang_rob, ang_ref)                                                                    # set off_course_flag

    # Control logic
    if off_cource_flag:
        posistion_controller.clear()                                                            # Reset posistion controller
        pos_ctrl_output = 0
        angle_controller.setSetpoint(ang_ref)                                                   # Set setpoint for angle
        ang_ctrl_output = angle_controller.update(ang_rob)                                      # Update controller
        ang_ctrl_output = ang_ctrl_output - (ang_ctrl_output % SCALE_FACTOR)
        diagnostics(ang_ctrl_output, ang_rob, dist_rob, pos_ctrl_output, ang_ref)


    # Posistion controller
    else:
        angle_controller.clear()                                                                # Reset angle controller
        ang_ctrl_output = 0
        pos_ctrl_output = posistion_controller.update(dist_rob)
        pos_ctrl_output = pos_ctrl_output - (pos_ctrl_output % SCALE_FACTOR)
        diagnostics(ang_ctrl_output, ang_rob, dist_rob, pos_ctrl_output, ang_ref)


    # Start motors
    if ang_ctrl_output != priv_turn:
        robot.walk_stop()                                                                       # Stop walking forward
        robot.turn_start(ang_ctrl_output)                                                       # Start turning

    if pos_ctrl_output != priv_forward:
        robot.turn_stop()                                                                       # Stop turning
        robot.walk_start(pos_ctrl_output)                                                       # Start walking forward

    # Remember output for next iteration
    priv_turn = ang_ctrl_output
    priv_forward = pos_ctrl_output


# old 
def update_waypoint(xrob, yrob, waypoints):
    xref = waypoints[0]
    yref = waypoints[1]

    xdelta = math.fabs(xref - xrob)
    ydelta = math.fabs(yref - yrob)

    if xdelta < THREASHOLD_COORDINATES and ydelta < THREASHOLD_COORDINATES:
        waypoints.pop(0)
        waypoints.pop(0)
    return waypoints


# TODO: Use this code in main to control motors
def update_motors():
    global priv_forward
    global priv_turn

    # Get waypoint list and coordinates
    waypoints = [0, 0, 10, 10]
    xrob = 0
    yrob = 0

    update_waypoint(xrob, yrob, waypoints)
    output = controlloop(0.0, 0.0, 10.0, 0)

    turn_speed = output[1]
    walk_speed = output[0]

    if turn_speed != priv_turn:
        robot.walk_stop()                                                                       # Stop walking forward
        robot.turn_start(turn_speed)                                                            # Start turning

    if walk_speed != priv_forward:
        robot.turn_stop()                                                                       # Stop turning
        robot.walk_start(walk_speed)                                                                # Start walking forward

    priv_turn = turn_speed
    priv_forward = walk_speed


while False:
    update_motors()

def diagnostics(ang_ctrl_output, ang_rob, dist_rob, pos_ctrl_output, ang_ref):
    print(
    "DISTANCE: " + str(dist_rob) + "\t-\tROBOT ANGLE: " + str(ang_rob) + "\tREFERANCE ANGLE: " + str(ang_ref) + "\tANGLE OFFSET: " + str(ang_rob-ang_ref) + "\t-\tPOSISTION_OUTPUT " + str(
        pos_ctrl_output) + "\tANGLE OUTPUT: " + str(ang_ctrl_output))
