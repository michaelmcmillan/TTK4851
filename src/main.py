import video.extractor as extr
from object_recognition.object_rec import*
from time import sleep

while True:
    extractor = extr.ImageStreamExtractor()
    im = extractor.extract_image()
    im = cv2.imdecode(np.asarray(bytearray(im.data)), -1)
    plt.imshow(im)
    plt.ion()
    plt.show()
    plt.draw()
    plt.pause(0.001)
    #sleep(.1)
