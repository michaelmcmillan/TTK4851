from unittest import TestCase, skip
import nxt.locator
import nxt.brick

class TestNXT(TestCase):

    @skip('hang on there')
    def test_nxt_can_use_the_bluetooth_driver(self):
        b = nxt.locator.find_one_brick(debug=True)
        name, host, signal_strength, user_flash = b.get_device_info() 
        print(name, host, signal_strength, user_flash)
