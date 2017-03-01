from unittest import TestCase, skip
from control_system.brick_class import Walker

class TestNXT(TestCase):

    def test_the_walker_can_move_forward(self):
        walker = Walker()
        walker.move()
