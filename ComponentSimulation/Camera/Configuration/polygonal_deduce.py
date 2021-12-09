import os.path

import matplotlib.pyplot as plt
from cv2 import cv2

img = cv2.imread(os.path.join(os.path.dirname(__file__),"SourceImage/B_LESS_CAR.png"))
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
plt.imshow(img)
plt.show()