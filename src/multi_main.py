from multiprocessing import Process, Queue, Value, Array, Manager, Pipe
from threading import Thread
from time import sleep
from matplotlib import pyplot as plt

from multiprocessing.managers import BaseManager

class Video(Process):

    def __init__(self):
        self.output = Value(c_char_p, '' * 8*1024*1024, lock=True) #create_lifo_queue()
        super(Video, self).__init__()

    def run(self):
        previous_image = None
        while True:
            image = image_extractor.latest_image
            if image != previous_image:
                print("got image")
                self.output = Value(c_char_p, image.data)
                previous_image = image

class ObjectRecognition(Process):
    
    def __init__(self, pipe):
        #self.input = Queue()
        self.output = Queue()
        super(ObjectRecognition, self).__init__()
        self.pipe = pipe

    def run(self):
        from object_recognition.object_rec import object_rec_byte, byte_to_image, read_image, object_rec_file
        from video.extractor import ImageStreamExtractor
        
        image_extractor = ImageStreamExtractor(camera_ip='192.168.0.100')
        image_extractor.start()

        previous_image = None
        while True:
            image = image_extractor.latest_image
            #image = "object_recognition/test_mini2.png"
            if image != previous_image:
                previous_image = image.data

                robot_position, track_matrix, all_positions, labeled_track_matrix \
                    = object_rec_byte(image.data)
                #robot_position, track_matrix, all_positions, labeled_track_matrix \
#                    = object_rec_file(image)
                recognized_track = (robot_position, track_matrix)
                print robot_position

                self.pipe.send((robot_position, track_matrix))

                plt.imshow(recognized_track[1])
                plt.ion()
                plt.show()
                plt.draw()
                plt.pause(0.001)

                self.output.put(recognized_track)


class AStar(Process):

    def __init__(self, goal, pipe):
        self.output = Queue()
        self.goal = goal
        self.pipe = pipe
        super(AStar, self).__init__()

    def run(self):
        from path_finding.Domain import Map
        from path_finding.PathFinder import AStar

        while True:
            robot_position, track_matrix = self.pipe.recv() 
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
                #print("no waypoints")
                continue

            waypoints = self.waypoints[:]
            waypoints = [(waypoints[x], waypoints[x+1]) \
                for x in range(0, len(waypoints), 2) \
                if (waypoints[x], waypoints[x+1]) != (0,0)] 
    
            controlloop((self.robot_x.value, self.robot_y.value), waypoints)

#video = Video()
#video.start()

parent_pipe, child_pipe = Pipe()

recognition = ObjectRecognition(child_pipe)
recognition.start()

a_star = AStar(goal=(235, 125), pipe=parent_pipe)#
a_star.start()

controller = Controller()
controller.start()

def first_loop():
    from object_recognition.object_rec import byte_to_image

    while True:
        #print('hello', video.output.value)

        #image = video.output.value
#        recognition.input.put(image)
        #plt.imshow(byte_to_image(image))
        #plt.ion()
        #plt.show()
        #plt.draw()
        #plt.pause(0.001)
        recognized_track = recognition.output.get()
        controller.robot_x = Value('i', recognized_track[0][0])
        controller.robot_y = Value('i', recognized_track[0][1])
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
