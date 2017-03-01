from unittest import TestCase, skip
from src.control_system.brick_class import Walker

class TestNXT(TestCase):

    def test_the_walker_can_retrieve_US(self):
        walker = Walker()
        from time import sleep
        while True:
            #sleep(0.03)
            distance = walker.ultrasonic()
            print(distance)

    def xtest_the_walker_can_move_forward(self):
        walker = Walker()
        #walker.move()
        compass = walker.compass()

        from time import sleep
        while True:
            sleep(1)

            heading = compass.get_heading()
            print("Output fra compass", heading)
