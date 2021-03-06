from unittest import TestCase, skip
#import bluetooth

class TestLightBlue:

    def test_light_blue(self):

        print("performing inquiry...")

        nearby_devices = bluetooth.discover_devices(
                duration=8, lookup_names=True, flush_cache=True, lookup_class=False)

        print("found %d devices" % len(nearby_devices))

        for addr, name in nearby_devices:
            try:
                print("  %s - %s" % (addr, name))
            except UnicodeEncodeError:
                print("  %s - %s" % (addr, name.encode('utf-8', 'replace')))
