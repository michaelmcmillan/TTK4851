from time import sleep
from unittest import TestCase, skip
from os.path import join, dirname
from video.extractor import ImageStreamExtractor
from copy import copy

class TestImageExtraction(TestCase):

    stream_fixture = join(
        dirname(__file__),
        'fixtures',
        'http_camera_low_resolution_mpjeg.stream'
    )

    def test_it_pushes_images_to_a_list_as_they_appear(self):
        fake_stream = open(self.stream_fixture)
        extractor = ImageStreamExtractor(stream=fake_stream)

        # Wait for images to be extracted
        extractor.start()
        sleep(0.150)
        extractor.stop()

        self.assertNotEqual(extractor.images, [])

    def test_it_can_return_the_latest_image_it_found(self):
        fake_stream = open(self.stream_fixture)
        extractor = ImageStreamExtractor(stream=fake_stream)

        # Wait for images to be extracted
        extractor.start()
        sleep(0.150)
        extractor.stop()

        latest_image = extractor.latest_image
        last_image = extractor.images[len(extractor.images)-1]

        self.assertEqual(latest_image, last_image)

    def test_latest_image_changes_if_stream_restarts(self):
        fake_stream = open(self.stream_fixture)
        extractor = ImageStreamExtractor(stream=fake_stream)

        # Wait for images to be extracted
        extractor.start()
        sleep(0.150)
        extractor.stop()
        latest_image_then = copy(extractor.latest_image)

        # Wait some more for images to be extracted
        extractor.start()
        sleep(0.150)
        extractor.stop()
        latest_image_now = copy(extractor.latest_image)

        self.assertNotEqual(latest_image_now, latest_image_then)

    def test_it_finds_2_jpegs_in_the_http_stream(self):
        extractor = ImageStreamExtractor(camera_ip='192.168.0.100')

        # Wait for images to be extracted
        extractor.start()
        sleep(0.150)
        extractor.stop()

        self.assertNotEqual(extractor.images, [])
