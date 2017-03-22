from video.extractor import ImageStreamExtractor
from object_recognition.object_rec import *
from time import sleep

class Main:

    def __init__(self):
        self.image_extractor = ImageStreamExtractor()

    def start(self):
        '''Fires up each module.'''
        self.image_extractor.start()

    def from_camera_to_object_recognition(self):
        '''Fetches image from camera and feeds it to the object recognizer.'''
        image = self.image_extractor.latest_image
        if not image:
            return

        robot_position, track_matrix, all_positions, labeled_track_matrix \
            = object_rec_byte(image.data)

        return (robot_position, track_matrix)

    def from_object_recognition_to_a_star(self):
        robot_position, track_matrix = self.from_camera_to_object_recognition()
        print(robot_position, track_matrix)
        
main = Main()
main.start()
sleep(0.5)

main.from_object_recognition_to_a_star()

while False:
    sleep(1)
    extractor.latest_image
    sleep(1)

    #im = extractor.extract_image()
    #im = cv2.imdecode(np.asarray(bytearray(im.data)), -1)
#
    #plt.imshow(im)
    #plt.ion()
    #plt.show()
    #plt.draw()
    #plt.pause(0.001)
