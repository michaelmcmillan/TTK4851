from multiprocessing import Process, Queue, Value, Array, Manager
from threading import Thread
from time import sleep
from matplotlib import pyplot as plt

# This code implements a shared LifoQueue.

from multiprocessing.managers import BaseManager
from Queue import LifoQueue

class LifoManager(BaseManager):
    pass

LifoManager.register('LifoQueue', LifoQueue)
def create_lifo_queue():
    manager = LifoManager()
    manager.start()
    return manager.LifoQueue()

class Video(Process):

    def __init__(self):
        self.output = Queue()#create_lifo_queue()
        super(Video, self).__init__()

    def run(self):
        from video.extractor import ImageStreamExtractor
        

        image_extractor = ImageStreamExtractor(camera_ip='192.168.0.101')
        image_extractor.start()
        previous_image = None
        while True:
            image = image_extractor.latest_image
            if image != previous_image:
                #print('Image extracted from video stream.')
                self.output.put(image.data)
                if self.output.qsize() < 2:
                    pass
                else:
                    self.output.get()

                previous_image = image

class ObjectRecognition(Process):
    
    def __init__(self):
        self.input = Queue()
        self.output = Queue()
        super(ObjectRecognition, self).__init__()

    def run(self):
        from object_recognition.object_rec import object_rec_byte, byte_to_image

        while True:
            image = self.input.get()
            #print('Object recognition: Received image.')
            robot_position, track_matrix, all_positions, labeled_track_matrix \
                = object_rec_byte(image)
            recognized_track = (robot_position, track_matrix)
            #plt.imshow(track_matrix, cmap="gray")
            self.output.put(recognized_track)
            #print('Object recognition: Pushed matrix.')

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
            print('A*: Received matrix.')
            map_ = Map(track_matrix, robot_position, self.goal)
            a_star = AStar(map_, 'BestFS')
            waypoints = a_star.best_first_search()
            self.output.put(waypoints) 
            print('A*: Pushed waypoints.')

class Controller(Process):

    def __init__(self):
        self.robot_x = Value('i', -1)
        self.robot_y = Value('i', -1)
        self.waypoints = Array('i', 1000)
        super(Controller, self).__init__()

    def run(self):
        from control_system.controlloop import controlloop

        while True:
            sleep(0.10)
            if self.waypoints[:][0] == 0:
                print("no waypoints")
                continue

            waypoints = self.waypoints[:]
            waypoints = [(waypoints[x], waypoints[x+1]) \
                for x in range(0, len(waypoints), 2) \
                if (waypoints[x], waypoints[x+1]) != (0,0)] 

#            controlloop((self.robot_x.value, self.robot_y.value), waypoints)

video = Video()
video.start()

recognition = ObjectRecognition()
recognition.start()

a_star = AStar(goal=(100, 200))
a_star.start()

controller = Controller()
controller.start()

def first_loop():
    from object_recognition.object_rec import byte_to_image
    while True:
        image = video.output.get()
#        recognition.input.put(image)
        plt.imshow(byte_to_image(image))
        plt.ion()
        plt.show()
        plt.draw()
        plt.pause(0.001)
#        recognized_track = recognition.output.get()
#        controller.robot_x = Value('i', recognized_track[0][0])
#        controller.robot_y = Value('i', recognized_track[0][1])
#        a_star.input.put(recognized_track)

def second_loop():
    while True:
        waypoints = a_star.output.get()
        controller.waypoints = Array('i', [i for coordinate in waypoints for i in coordinate])

t1 = Thread(target=first_loop)
t2 = Thread(target=second_loop)
t1.setDaemon(True)
t2.setDaemon(True)
t1.start()
t2.start()
