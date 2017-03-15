import hashlib
from base64 import b64encode
from httplib import HTTPConnection

class Image:

    def __init__(self, data):
        self.data = data

    @property
    def name(self):
        return hashlib.sha224(self.data).hexdigest()[:6]

    def save(self, name):
        with open('/tmp/video/%s.jpg' % name, 'w') as f:
            f.write(self.data)

    def __repr__(self):
        return '<Image name=%s, size=%d>' % (self.name, len(self.data))

class ImageStreamExtractor:

    def __init__(self, stream=None):
        self.stream = stream \
            if stream else self.get_stream_from_camera()

    def get_stream_from_camera(self):
        conn = HTTPConnection('192.168.0.100')
        authorization = {'Authorization': 'Basic YWRtaW46'} # admin, blank
        conn.request('GET', '/video/mjpg.cgi?profileid=3', headers=authorization)
        return conn.getresponse()

    @staticmethod
    def get_data(src, chunk_size=1024*10):
        d = src.read(chunk_size)
        while d:
            yield d
            d = src.read(chunk_size)

    def extract_image(self):
        feed_me = False
        data = self.get_data(self.stream)
        image = ''

        for chunk in data:

            for byte_number, byte in enumerate(chunk):

                # START image
                if  chunk[byte_number]   == '\xff' \
                and chunk[byte_number+1] == '\xd8' \
                and chunk[byte_number+2] == '\xff' \
                and chunk[byte_number+3] == '\xdb':
                    feed_me = True 

                # EOF image
                if  chunk[byte_number]   == '\xff' \
                and chunk[byte_number+1] == '\xd9' \
                and chunk[byte_number+2] == '\xff' \
                and chunk[byte_number+3] == '\xd9' \
                and chunk[byte_number+4] == '\x0d' \
                and chunk[byte_number+5] == '\x0a':
                    feed_me = False

                if feed_me:
                    image += byte

                if image and not feed_me:
                    return Image(data=image)
