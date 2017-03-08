import hashlib
from base64 import b64encode

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

    def __init__(self, stream):
        self.stream = stream

    def extract_latest_image(self):
        recent_images = self.extract_images()
        latest_image = recent_images[len(recent_images) - 1]
        return latest_image

    def extract_images(self):
        images = []
        start, stop = None, None
        chunk = self.stream.read(1024*5)

        for byte_number, byte in enumerate(chunk):

            # START image
            if  chunk[byte_number]   == '\xff' \
            and chunk[byte_number+1] == '\xd8' \
            and chunk[byte_number+2] == '\xff' \
            and chunk[byte_number+3] == '\xdb':
                start = byte_number

            # EOF image
            if  chunk[byte_number]   == '\xff' \
            and chunk[byte_number+1] == '\xd9' \
            and chunk[byte_number+2] == '\xff' \
            and chunk[byte_number+3] == '\xd9' \
            and chunk[byte_number+4] == '\x0d' \
            and chunk[byte_number+5] == '\x0a':
                stop = byte_number

            # When we have a start and a stop
            if start and stop:
                image = Image(data=chunk[start:stop])
                images.append(image)
                start, stop = None, None 

        return images
