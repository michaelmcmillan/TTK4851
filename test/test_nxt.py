from unittest import TestCase, skip
from control_system.brick_class import Walker

class TestNXT(TestCase):

    def test_nxt_can_use_the_bluetooth_driver(self):
        walker = Walker()
        walker.move()
