import math
import controller
import pidvariables
import brick_class
import nxt_functions

# Create flags for desicions
waypoint_flag = False
off_cource_flag = False
THREASHOLD_POS = 2
THREASHOLD_ANG = 2
SAMPLE_TIME = 0.1

# Create PID variables
PIDvar = pidvariables.PidVariables()

# Create Controllers
posistion_controller = controller.PID(2.5, .1, 1.5)
posistion_controller.setSampleTime(SAMPLE_TIME)
posistion_controller.setSetpoint(0)

angle_controller = controller.PID(2.5, .1, 0)
angle_controller.setSampleTime(SAMPLE_TIME)

walker=brick_class.Walker()


while True:
    # Update coordinates
    PIDvar.update_coordinates()

    # Get robot/ref distance and angle
    dist_rob = PIDvar.get_dist_robot()
    ang_rob = PIDvar.get_ang_robot()                                      # From Compass
    ang_ref = PIDvar.get_ang_ref()                                        # Calculated from coordinates
    print(ang_rob)
    ang_offset = math.fabs(ang_rob)-math.fabs(ang_ref)                  # Offset in angle

    # Angle controller
    if ang_offset > THREASHOLD_ANG:
        posistion_controller.clear()                                    # Reset posistion controller
        ang_ctrl_output = angle_controller.update(ang_rob)# Update controller
        walker.turn(SAMPLE_TIME,ang_ctrl_output)


    # Posistion controller
    else:
        angle_controller.clear()                                        # Reset angle controller
        pos_ctrl_output = posistion_controller.update(PIDvar.get_dist_robot)              # Update posistion controller
        walker.move(SAMPLE_TIME,pos_ctrl_output)
        # TODO: apply controller output to robot

    # Check waypoint (Without interupt)
    # TODO: check if waypoint matrix is been updated (Without interupt)
    if dist_rob < THREASHOLD_POS:                                       #check if robot has reached the waypoint
        PIDvar.set_new_waypoint()
        pass

