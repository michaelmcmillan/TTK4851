import math
import controller
import pidvariables


# Create PID variables
PIDvar = pidvariables(0)

# Create Controllers
posistion_controller = controller.PID(2.5, .1, 1.5)
posistion_controller.setSampleTime(0.1)

angle_controller = controller.PID(2.5, .1, 0)
angle_controller.setSampleTime(0.1)

# Create flags for desicions
waypoint_flag = False
off_cource_flag = False


while():

    #Update waypoint
    if math.fabs(PIDvar.get_dist_robot) < 1:                            # Robot is at origo
        PIDvar.set_new_waypoint()                                       # Updating waypoint coordinates

        angle_controller.setSetpoint(PIDvar.ang_ref)                    # New setpoint for angle controller
        posistion_controller.setSetpoint(0)                             # setpoint is always origo

    # check if robot is on course
    #Choose regulator
    if off_cource_flag:
        posistion_controller.clear()                                # Reset posistion controller
        angle_controller.update(PIDvar.get_ang_robot)               # update angle controller

    else:
        angle_controller.clear()                                    # Reset angle controller
        posistion_controller.update(PIDvar.get_dist_robot)           # Update posistion controller





# Test variables for calculations
Xac = 0
Yac = 0
xref = 5
Yref = 5
compass = 0

