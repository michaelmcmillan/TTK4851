from httplib import HTTPConnection
from unittest import TestCase, skip
from os.path import join, dirname
from video.extractor import ImageStreamExtractor

class TestImageExtraction(TestCase):

    stream_fixture = join(
        dirname(__file__),
        'fixtures',
        'http_camera_low_resolution_mpjeg.stream'
    )

    def test_it_finds_2_jpegs_from_fake_stream_on_disk(self):
        with open(self.stream_fixture) as fake_stream:
            extractor = ImageStreamExtractor(stream=fake_stream)
            images = extractor.extract_images()
            self.assertEqual(len(images), 2)

    def test_latest_image_returns_the_most_recent(self):
        with open(self.stream_fixture) as fake_stream:
            extractor = ImageStreamExtractor(stream=fake_stream)
            latest_image = extractor.extract_latest_image()
            self.assertEqual(latest_image.name, '40b437')

    def test_it_finds_2_jpegs_in_the_http_stream(self):
        conn = HTTPConnection('192.168.0.100')
        authorization = {'Authorization': 'Basic YWRtaW46'} # admin, blank
        conn.request('GET', '/video/mjpg.cgi?profileid=3', headers=authorization)
        real_stream = conn.getresponse()

        extractor = ImageStreamExtractor(stream=real_stream)
        images = extractor.extract_images()
        self.assertEqual(len(images), 2)
