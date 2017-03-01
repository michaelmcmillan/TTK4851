from time import sleep
from nxt.brick import Brick
from nxt.locator import find_one_brick
from nxt.motor import Motor, PORT_A, PORT_B
<<<<<<< HEAD
from nxt.sensor import Ultrasonic, PORT_1
from nxt.sensor import hitechnic, PORT_2            #TEST
=======
from nxt.sensor import Ultrasonic, PORT_1, MSCompassv2, PORT_2, PORT_3
>>>>>>> 2f4a7f8f1012d62adf30fd403d195d3a746a1e98

''' Object for a simple agent using the NXT interface. Makes it possible for th agent to move and turn based on inputs  '''
class Walker(object):
    ''' Initialize a brick with it's two motors for moving. By default looks for the name "NXT" if no name is given '''
    def __init__(self, brick="NXT"):
        if isinstance(brick, basestring):
            brick = find_one_brick(name=brick)
        self.brick = brick
        self.motor = True
        self.sensor = True
        try:
            self.brick = brick
        except:
            print("No brick found")
        try:
            self.wheels = [Motor(brick, PORT_A), Motor(brick, PORT_B)]
        except:
            self.motor = False
            print("No motors detected!")
        #try:
            #self.bat_eyes = Ultrasonic(brick, PORT_1)
        #except Exception as e:
            #self.sensor = False
            #print("No sensor found")

    '''Retrieve compass data'''
    def ultrasonic(self):
        us = Ultrasonic(self.brick, PORT_3)
        return us.get_distance()

<<<<<<< HEAD
        # Compass EXPERIMENTS
        try:
            self.read_compass = hitechnic.Compass(brick, PORT_2)
        except Exception as e:
            self.sensor = False
            print(e)
            print("No sensor found")

=======
    '''Retrieve compass data'''
    def compass(self):
        compass = MSCompassv2(self.brick, PORT_3)
        return compass
>>>>>>> 2f4a7f8f1012d62adf30fd403d195d3a746a1e98

    ''' Lets the agent move forward or backwards for the given time in seconds and with the speed/power given '''
    def move(self, seconds, speed):
        if self.motor:
            for motor in self.wheels:
                motor.run(power=speed)
            sleep(seconds)
            for motor in self.wheels:
                motor.idle()
        else:
            print("You have no motors!")
    ''' Makes the agent turn for a given amount of time in seconds, and with the given speed/power '''
    def turn(self, seconds, speed):
        if self.motor:
            self.wheels[0].run(power=speed)
            self.wheels[1].run(power=-speed)

            sleep(seconds)

            for motor in self.wheels:
                motor.idle()
        else:
            print("You have no motors!")
    def bat_mode(self):
        if self.sensor:
            return self.ultrasonic.get_sample()
        else:
            print("You have no eyes!")
            return -1
    # TEST
    def read_compass(self):
        return self.compass.get_sample()

if __name__=="__main__":
    b = Walker()
