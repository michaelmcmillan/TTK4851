from multiprocessing import Process, Queue, Value
from threading import Thread
from time import sleep

# This code implements a shared LifoQueue.

#from multiprocessing.managers import BaseManager
#from Queue import LifoQueue

#class LifoManager(BaseManager):
#    pass

#LifoManager.register('LifoQueue', LifoQueue)
#manager = LifoManager()
#manager.start()
#self.output = manager.LifoQueue()

class Video(Process):

    def __init__(self):
        self.output = Queue() 
        super(Video, self).__init__()

    def run(self):
        from video.extractor import ImageStreamExtractor

        image_extractor = ImageStreamExtractor(camera_ip='192.168.0.102')
        image_extractor.start()
        previous_image = None

        while True:
            image = image_extractor.latest_image
            if image != previous_image:
                self.output.put(image.data)
                previous_image = image

class ObjectRecognition(Process):
    
    def __init__(self):
        self.input = Queue()
        self.output = Queue()
        super(ObjectRecognition, self).__init__()

    def run(self):
        from object_recognition.object_rec import object_rec_byte

        while True:
            image = self.input.get()
            robot_position, track_matrix, all_positions, labeled_track_matrix \
                = object_rec_byte(image)
            recognized_track = (robot_position, track_matrix)
            self.output.put(recognized_track)

class AStar(Process):

    def __init__(self, goal):
        self.input = Queue()
        self.output = Queue()
        self.goal = goal
        super(AStar, self).__init__()

    def run(self):
        from path_finding.Domain import Map
        from path_finding.PathFinder import AStar

        while True:
            robot_position, track_matrix = self.input.get() 
            map_ = Map(track_matrix, robot_position, self.goal)
            a_star = AStar(map_, 'BestFS')
            waypoints = a_star.best_first_search()
            self.output.put(waypoints) 

class Controller(Process):

    def __init__(self):
        self.robot_x = Value('i', -1)
        self.robot_y = Value('i', -1)
        self.waypoints = None
        super(Controller, self).__init__()

    def run(self):
        while True:
            sleep(0.1)
            print(self.robot_x, self.robot_y)

video = Video()
video.start()

recognition = ObjectRecognition()
recognition.start()

a_star = AStar(goal=(100, 200))
a_star.start()

controller = Controller()
controller.start()

def first_loop():
    while True:
        image = video.output.get()
        recognition.input.put(image)
        recognized_track = recognition.output.get()
        controller.robot_x = Value('i', recognized_track[0][0])
        controller.robot_y = Value('i', recognized_track[0][1])
        a_star.input.put(recognized_track)

def second_loop():
    while True:
        waypoints = a_star.output.get()
        print("got waypoints")
        controller.waypoints = waypoints

t1 = Thread(target=first_loop)
t2 = Thread(target=second_loop)
t1.setDaemon(True)
t2.setDaemon(True)
t1.start()
t2.start()

#while True:

    # Thread 1

    # Thread 2
