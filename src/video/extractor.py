from datetime import datetime
import hashlib
from base64 import b64encode
from httplib import HTTPConnection
import threading

class Image:
    '''Represents a JPEG.'''

    def __init__(self, data):
        self.data = data

    @property
    def name(self):
        return hashlib.sha224(self.data).hexdigest()[:6]

    def save(self, name=None):
        name = datetime.now()
        with open('/tmp/video/%s.jpg' % name, 'w') as f:
            f.write(self.data)

    def __repr__(self):
        return '<Image name=%s, size=%d>' % (self.name, len(self.data))

class ImageStreamExtractor:
    '''Asynchronously parses a stream of JPEGs.'''

    def __init__(self, stream=None, camera_ip=None):
        self.images = []
        self.latest_image = None
        self.worker = threading.Thread(target=self.extract_image)
        self.camera_ip = camera_ip
        self.stream = stream \
            if stream else self.get_stream_from_camera()
        self.working = False

    def start(self):
        '''Spin up a thread that parses the stream for images.'''
        self.working = True
        self.worker.start()

    def stop(self):
        '''Terminate the thread that parses images.'''
        self.working = False
        self.worker = threading.Thread(target=self.extract_image)

    def get_stream_from_camera(self):
        '''Open a HTTP stream to the DLink webcam.'''
        conn = HTTPConnection(self.camera_ip)
        # Username: admin. Password: <blank>
        authorization = {'Authorization': 'Basic YWRtaW46'}
        conn.request('GET', '/video/mjpg.cgi?profileid=3', headers=authorization)
        return conn.getresponse()

    @staticmethod
    def get_stream(src, chunk_size=1024*10):
        '''Spits out bytes from the stream in chunks of 10kb.'''
        d = src.read(chunk_size)
        while d:
            yield d
            d = src.read(chunk_size)

    def extract_image(self):
        '''Pushes extracted images from stream to the images list.'''

        # A flag that indicates if we've found an image or not.
        collecting_bytes = False

        # This will eventually contain a single image.
        image_data = ''

        # Process the stream in chunks of 10kb.
        for chunk in self.get_stream(self.stream):

            # Stop thread if we've been told so.
            if not self.working:
                return

            for byte_number, byte in enumerate(chunk):

                try:

                    # Start: Magic byte that signalizes JPEG start
                    if  chunk[byte_number]   == '\xff' \
                    and chunk[byte_number+1] == '\xd8' \
                    and chunk[byte_number+2] == '\xff' \
                    and chunk[byte_number+3] == '\xdb':
                        collecting_bytes = True 

                    # Stop: EOF byte that signalizes JPEG stop
                    if  chunk[byte_number]   == '\xff' \
                    and chunk[byte_number+1] == '\xd9' \
                    and chunk[byte_number+2] == '\xff' \
                    and chunk[byte_number+3] == '\xd9' \
                    and chunk[byte_number+4] == '\x0d' \
                    and chunk[byte_number+5] == '\x0a':
                        collecting_bytes = False

                # Reset everything if error occured while parsing
                except IndexError:
                    image_data = ''
                    collecting_bytes = False
                    break

                # Add byte to image now that we are inbetween start and stop.
                if collecting_bytes:
                    image_data += byte

                # Push image to images if it is an image and JPEG stop was found.
                if image_data and not collecting_bytes:
                    parsed_image = Image(data=image_data)
                    self.latest_image = parsed_image
                    self.images.append(parsed_image)
                    image_data = ''
