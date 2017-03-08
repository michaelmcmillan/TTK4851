import robot
import time

while True:
    compass = robot.read_compass()
    ultra = robot.read_ultrasonic()
    print("Compass: " + str(compass))
    print("Distance: " + str(ultra))
    time.sleep(3)
