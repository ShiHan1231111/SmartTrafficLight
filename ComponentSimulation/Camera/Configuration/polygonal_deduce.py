import os.path

import matplotlib.pyplot as plt
from cv2 import cv2

img = cv2.imread("traffic003.jpg")
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
plt.imshow(img)
plt.show()