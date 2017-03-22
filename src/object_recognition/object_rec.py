from os import path
import numpy as np
import cv2
from matplotlib import pyplot as plt
from time import time
from scipy import ndimage as ndi

def read_image(filepath="test_mini2.png"):
    image = cv2.imread(filepath)
    return image
def byte_to_image(image_data):
    return cv2.imdecode(np.asarray(bytearray(image_data)), -1)
def fill_image(im):
    h, w = im.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    imf = im.copy()
    cv2.floodFill(imf, mask, (0,0), 255)
    im_flodf = cv2.bitwise_not(imf)
    im2 = im | im_flodf
    return im2
def find_centers(image, stride_x=10, stride_y=10):
    centers = []

    label_objects, nb_labels = ndi.label(image)

    coords_x  = {}
    coords_y  = {}
    for i in range(nb_labels):
        coords_x[i+1] = []
        coords_y[i+1] = []

    for x in range(0, len(image), stride_x):
        for y in range(0, len(image[x]), stride_y):
            if label_objects[x, y] == 0:
                pass
            else:
                coords_x[label_objects[x,y]].append(x)
                coords_y[label_objects[x,y]].append(y)
    for i in range(nb_labels):
        if coords_x[i+1] and coords_y[i+1]:
            centers.append((int(np.median(coords_x[i+1])), int(np.median(coords_y[i+1]))))
    return centers, label_objects
def segment_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    kernel = np.ones((3, 3))
    image = cv2.Canny(image[:,:,2], 90, 130, L2gradient=True)
    image = cv2.dilate(image, kernel, iterations=2)
    image = cv2.erode(image, kernel, iterations=1)
    image = fill_image(image)
    label_objects, nb_labels = ndi.label(image)
    sizes = np.bincount(label_objects.ravel())
    mask_sizes = sizes > 100
    mask_sizes[0] = 0
    image = mask_sizes[label_objects]
    centers, labeled_image = find_centers(image)
    return image, centers, labeled_image
def find_robot(image, template):
    res  = cv2.matchTemplate(image, template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    h,w = template.shape[:2]
    bottom_right = (top_left[0] + w, top_left[1] + h)
    coord_x = int(np.mean(np.array([x for x in range(top_left[0], bottom_right[0]+1)])))
    coord_y = int(np.mean(np.array([x for x in range(top_left[1], bottom_right[1]+1)])))
    coords = (coord_y, coord_x)
    return coords
""" Call this function for segmenting an image from a list of bytes  """
def object_rec_byte(byte_image):
    image = byte_to_image(byte_image)
    return object_rec_main(image)
""" Call this function for segmenting an image from file """
def object_rec_file(file_name = "test_mini2.png"):
    image = read_image(file_name)
    return object_rec_main(image)

def object_rec_main(image):
    cimage, centers, labeled_image = segment_image(image)
    robot_pos = find_robot(image, template)
    if labeled_image[robot_pos] != 0:
        robot_pos = centers[labeled_image[robot_pos]-1]
    return robot_pos, cimage, centers, labeled_image

dir_of_template = path.dirname(__file__)
template = read_image(path.join(dir_of_template, "mini_template.png"))

if __name__=="__main__":
    robot_pos, cimage, centers, labeled_image = object_rec_file()
    stop = time()
    """image = read_image()
    start = time()
    cimage, centers, labeled_image = segment_image(image)
    robot_pos = find_robot(image, template)
    if labeled_image[robot_pos] != 0:
        robot_pos = centers[labeled_image[robot_pos]-1]
    print(time()-start)
    print robot_pos
    #plt.imshow(labeled_image)
    #np.save("labeled_matrix", labeled_image)
    #np.save("binary_matrix", cimage)
    """
    #plt.imshow(cimage, cmap="gray")
    #plt.show()
