r'''Alpha Rex API

    A high-level, object-oriented programming interface to Lego MINDSTORMS
    NXT's "Alpha Rex" model (see [1] for assembling instructions), along with a
    small collection of functions demonstrating obvious usage scenarios.

    1. http://www.active-robots.com/products/mindstorms4schools/building-instructions.shtml
'''

from time import sleep

from nxt.brick import Brick
from nxt.locator import find_one_brick
from nxt.motor import Motor, PORT_A, PORT_B, PORT_C
from nxt.sensor import Light, Sound, Touch, Ultrasonic, HTCompass
from nxt.sensor import PORT_1, PORT_2, PORT_3, PORT_4


FORTH = 100
BACK = -100


class Seng(object):
    def __init__(self, brick='NXT'):
        r'''Creates a new Alpha Rex controller.

            brick
                Either an nxt.brick.Brick object, or an NXT brick's name as a
                string. If omitted, a Brick named 'NXT' is looked up.
        '''
        if isinstance(brick, basestring):
            brick = find_one_brick(name=brick)

        self.brick = brick
        self.arms = Motor(brick, PORT_C)
        self.left = Motor(brick, PORT_A)
        self.right = Motor(brick, PORT_B)

        self.direction = HTCompass(brick, PORT_2)
        self.ultrasonic = Ultrasonic(brick, PORT_4)

    def echolocate(self):
        r'''Reads the Ultrasonic sensor's output.
        '''
        return self.ultrasonic.get_sample()

    def compass(self):
        return self.direction.get_sample()

    def walk_seng(self, secs, power):
        r'''Simultaneously activates the leg motors, causing Alpha Rex to walk.

            secs
                How long the motors will rotate.

            power
                The strength effected by the motors. Positive values will cause
                Alpha Rex to walk forward, while negative values will cause it
                to walk backwards. If you are unsure about how much force to
                apply, the special values FORTH and BACK provide reasonable
                defaults. If omitted, FORTH is used.
        '''

        self.left.run(power=power)
        self.right.run(power=power)

        sleep(secs)
        self.left.idle()
        self.right.idle()

    def turn_seng(self, secs, power):
        self.left.run(power=power)
        self.right.run(power=-power)

        sleep(secs)
        self.left.idle()
        self.right.idle()


robot = Seng()


def read_ultrasonic():
    r'''Connects to a nearby Alpha Rex, then commands it to walk forward and
           then backwards.
       '''
    return robot.echolocate()

def walk_forth_and_back():
    r'''Connects to a nearby Alpha Rex, then commands it to walk forward and
        then backwards.
    '''
    robot.walk(10, FORTH)
    robot.walk(10, BACK)

def walk(secs,speed):
    robot.walk_seng(secs, -speed)

def turn(secs,speed):
    robot.turn_seng(secs, -speed)

def walk_to_object():
    r'''Connects to a nearby Alpha Rex, then commands it to walk until it
        approaches an obstacle, then stop and say 'Object' three times.
    '''
    while robot.echolocate() > 10:
        robot.walk(1, FORTH)

    robot.say('Object', 3)


def read_compass():
    return robot.compass()

if __name__ == '__main__':
    walk_to_object()

