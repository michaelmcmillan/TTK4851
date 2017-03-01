from unittest import TestCase, skip
from src.control_system.brick_class import Walker

class TestNXT(TestCase):

    def get_heading(self):
        walker = Walker()
        heading = walker.compass()
        return heading

    def get_distance(self):
        walker = Walker()
        dist = walker.ultrasonic()
        return dist

    def xtest_the_walker_can_move_forward(self):
        walker = Walker()
        walker.move()
        compass = walker.compass()

        from time import sleep
        while True:
            sleep(1)

            heading = compass.get_heading()
            print("Output fra compass", heading)

