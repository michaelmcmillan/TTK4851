from PIL import Image
import numpy as np
#import GenericSearchNode
from PathFinder import *
from Domain import *

from time import time
import os
import webbrowser


def main():

    pixels = np.load("binary_matrix.npy")
    map = Map(pixels, [0,0], [23,167])
    #map.printMap()
    #start = time()
    #print (map.map[50,40].g)
    pathSpace = AStar(map, "BestFS", stride = 1)
    start = time()
    pathSpace.best_first_search()
    print ("Execution time with stride = 1: ", time() - start)

    pathSpace = AStar(map, "BestFS", stride=5)
    start = time()
    pathSpace.best_first_search()
    print("Execution time with stride = 5: ", time() - start)

    #binCameraImage = np.load('binary_matrix.npy')
    #print binCameraImage.shape
    #pixels = Image.new('1', binCameraImage.shape)
    #pixels = img.load()

    # for i in range(pixels.size[0]):
    #      for j in range(pixels.size[1]):
    #          pixelValue = binCameraImage[i][j]
    #          pixels[i,j] = int(pixelValue)
    # print pixels[5,5]
    # pixels.save('robot_bw_view.png')
    # webbrowser.open('robot_bw_view.png')



main()

