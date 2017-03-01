import numpy as np
import cv2
from matplotlib import pyplot as plt
from time import time

def fill_image(im):
    h, w = im.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    im2, conts, hir = cv2.findContours(im, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(im2, conts, -1, (255, 255, 0), -1)
    print im2.shape
    return im2
image = cv2.imread("Skjermbilde 2017-02-15 kl. 13.09.14.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
kernel = np.ones((3, 3))
image = cv2.Canny(image[:,:,2], 50, 130, L2gradient=True)
image = cv2.dilate(image, kernel, iterations=3)
image = cv2.erode(image, kernel, iterations=2)
image = fill_image(image)
plt.imshow(image, cmap="gray")
plt.show()
