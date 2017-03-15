import math
import controller
import pidvariables
import robot

# Create flags for desicions
waypoint_flag = False
off_cource_flag = False
THREASHOLD_POS = 2
THREASHOLD_ANG_MAX = 15
THREASHOLD_ANG_MIN = 5
SAMPLE_TIME = 0.1
ROBOT_LENGHT = 13

# Create PID variables
PIDvar = pidvariables.PidVariables()

# Create Controllers
posistion_controller = controller.PID(5.5, 2, 1.5)
posistion_controller.setSampleTime(SAMPLE_TIME)
posistion_controller.setSetpoint(0)

angle_controller = controller.PID(0.5, 1, 0)
angle_controller.setSampleTime(SAMPLE_TIME)

ang_ctrl_output = 0
pos_ctrl_output = 0

while True:
    # Update coordinates
    PIDvar.update_coordinates()

    # Get robot/ref distance and angle
    dist_rob = PIDvar.get_dist_robot() - ROBOT_LENGHT
    ang_rob = robot.read_compass()                                          # From Compass
    ang_ref = PIDvar.get_ang_ref()                                          # Calculated from coordinates
    ang_offset = math.fabs(ang_rob)-math.fabs(ang_ref)                      # Offset in angle

    # Offset logic
    if math.fabs(ang_offset) > THREASHOLD_ANG_MAX:
        off_cource_flag = False
    if math.fabs(ang_offset) < THREASHOLD_ANG_MIN:  # Check offset
        off_cource_flag = False

    # Angle controller
    if off_cource_flag:
        posistion_controller.clear()                                        # Reset posistion controller
        pos_ctrl_output = posistion_controller.output
        ang_ctrl_output = angle_controller.update(ang_rob)                  # Update controller
        #robot.turn(SAMPLE_TIME, int(ang_ctrl_output))
        # TODO: vurder a sett motorene inni controller.update for a ikke belaste motoren sa mye


    # Posistion controller
    else:
        angle_controller.clear()                                            # Reset angle controller
        ang_ctrl_output = angle_controller.output
        pos_ctrl_output = posistion_controller.update(dist_rob)             # Update posistion controller
        robot.walk(SAMPLE_TIME, int(pos_ctrl_output))
        # TODO: vurder a sett motorene inni controller.update for a ikke belaste motoren sa mye

    # Check waypoint (Without interupt)
    # TODO: check if waypoint matrix is been updated (Without interupt)
    if dist_rob < THREASHOLD_POS:                                           #check if robot has reached the waypoint
        PIDvar.set_new_waypoint()
        pass

    print("DISTANCE: " + str(dist_rob) + "\tCOMPASS: " + str(ang_rob) + "\tANGLE OFFSET: " + str(ang_offset) + "\tPOSISTION_OUTPUT " + str(pos_ctrl_output) + "\t\t\tANGLE OUTPUT: " + str(ang_ctrl_output))