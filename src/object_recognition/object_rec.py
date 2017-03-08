import numpy as np
import cv2
from matplotlib import pyplot as plt
from time import time
from scipy import ndimage as ndi

def read_image(filepath="test.png"):
    image = cv2.imread(filepath)
    return image
def fill_image(im):
    h, w = im.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    imf = im.copy()
    cv2.floodFill(imf, mask, (0,0), 255)
    im_flodf = cv2.bitwise_not(imf)
    im2 = im | im_flodf
    print im2.shape
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
    image = cv2.Canny(image[:,:,2], 50, 130, L2gradient=True)
    image = cv2.dilate(image, kernel, iterations=2)
    image = cv2.erode(image, kernel, iterations=1)
    image = fill_image(image)
    label_objects, nb_labels = ndi.label(image)
    sizes = np.bincount(label_objects.ravel())
    mask_sizes = sizes > 1000
    mask_sizes[0] = 0
    image = mask_sizes[label_objects]
    centers, labeled_image = find_centers(image)
    print(centers)
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

if __name__=="__main__":
    start = time()
    image = read_image()
    template = read_image("robot_template.png")
    cimage, centers, labeled_image = segment_image(image)
    robot_pos = find_robot(image, template)
    if labeled_image[robot_pos] != 0:
        print labeled_image[robot_pos]
        robot_pos = centers[labeled_image[robot_pos]-1]
    print(time()-start)
    print robot_pos
    #plt.imshow(labeled_image)
    plt.imshow(cimage, cmap="gray")
    plt.show()
