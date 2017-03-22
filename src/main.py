from video.extractor import ImageStreamExtractor
from object_recognition.object_rec import *
from control_system.controlloop import controlloop
from time import sleep

class Main:

    def __init__(self):
        self.goal = (200, 300)
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
        '''Fetches robots position and track matrix from object recognizer
           and determines the shortest path from robots position to goal.'''
        robot_position, track_matrix = self.from_camera_to_object_recognition()
        print(robot_position, track_matrix)

    def from_a_star_to_controller(self):
        '''Fetches waypoints and robots position from A* and feeds that to
           the controller.'''
        robot_position = (0, 0)
        waypoints = [(100, 200)]  
        controlloop(robot_position, waypoints)

        # Kalles saa ofte som mulig, men akkurat naa funker samlebaand.
        # a_output = liste med waypoints hvor id = 0 foerste waypointen
        # (void) controlloop(robot_position, a_output)
        
if __name__ == '__main__':
    main = Main()
    main.start()

    # Give the camera some time to heat up
    sleep(0.5)

    #main.from_object_recognition_to_a_star()
    main.from_a_star_to_controller()
