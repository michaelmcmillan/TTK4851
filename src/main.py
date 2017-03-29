from video.extractor import ImageStreamExtractor
from object_recognition.object_rec import *
from control_system.controlloop import controlloop
from path_finding.Domain import Map
from path_finding.PathFinder import AStar
from skimage import img_as_ubyte

import cv2
from time import sleep


class Main:

    def __init__(self):
        self.goal = (40, 22)
        self.robot_position = (None, None)
        self.waypoints = []
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

        #cv2_compatible_track = img_as_ubyte(track_matrix)
        #cv2.imwrite('trackmatrix_fixed2.jpg', cv2_compatible_track))

        return (robot_position, track_matrix)

    def from_object_recognition_to_a_star(self):
        '''Fetches robots position and track matrix from object recognizer
           and determines the shortest path from robots position to goal.'''
        robot_position, track_matrix = self.from_camera_to_object_recognition()

        map_ = Map(track_matrix, robot_position, self.goal)

        print("starting a*")
        a_star = AStar(map_, 'BestFS')
        waypoints = a_star.best_first_search()
        print("stopping a*")

        return (robot_position, waypoints)

    def from_a_star_to_controller(self):
        '''Fetches waypoints and robots position from A* and feeds that to
           the controller.'''
        #robot_position = (100, 200)
        #waypoints = [(100, 200)]  


        robot_position, waypoints = self.from_object_recognition_to_a_star()

        # First waypoint is the robots location, which we dont care about
        waypoints.pop(0)

        while True:
            sleep(0.1)
            controlloop(robot_position, waypoints)

        # Kalles saa ofte som mulig, men akkurat naa funker samlebaand.
        # a_output = liste med waypoints hvor id = 0 foerste waypointen
        # (void) controlloop(robot_position, a_output)
        
if __name__ == '__main__':
    main = Main()
    main.start()

    # Give the camera some time to heat up
    sleep(0.5)

    #main.from_camera_to_object_recognition()
    main.from_a_star_to_controller()
