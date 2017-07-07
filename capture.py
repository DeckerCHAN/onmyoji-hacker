import cv2
import numpy as np
import pyautogui


class Capture(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def np_image(self):
        image = pyautogui.screenshot('/tmp/foo.png', region=(self.x, self.y, self.width, self.height))
        return np.asarray(image)


