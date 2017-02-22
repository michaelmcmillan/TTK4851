from unittest import TestCase
import lightblue

class TestLightBlue(TestCase):

    def test_light_blue(self):

        # ask user to choose the device to connect to
        hostaddr = lightblue.selectdevice()[0]        

        # find the EchoService advertised by the simple_server.py example
        echoservice = lightblue.findservices(addr=hostaddr, name="EchoService")[0]
        serviceport = echoservice[1]
