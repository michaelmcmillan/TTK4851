from unittest import TestCase, skip
from src.control_system.brick_class import Walker

class TestNXT(TestCase):

    def get_compass(self):
        walker = Walker()
        return walker.compass()
