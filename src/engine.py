from enum import Enum

import cv2
import numpy as np
import tensorflow as tf

from capture import Capture
from faster_rcnn.src.model.config import cfg
from faster_rcnn.src.nets.vgg16 import vgg16
from single_run import detect
from utils.common_utils import classes_from_file


class Running_mode(Enum):
    TRAIN = 1
    EVAL = 2


class Engine(object):
    def __init__(self, window, class_file, running_mode):
        self.classes = classes_from_file(class_file)
        self.window_x = window[0]
        self.window_y = window[1]
        self.window_width = window[2]
        self.window_height = window[3]

        self.capture = Capture(self.window_x, self.window_y, self.window_width, self.window_height)

        self.fast_rcnn = self.build_faster_rcnn_session()

    def build_faster_rcnn_session(self):
        tfconfig = tf.ConfigProto(allow_soft_placement=True)
        tfconfig.gpu_options.allow_growth = True
        # init session
        sess = tf.Session(config=tfconfig)
        net = vgg16(batch_size=1)

        net.create_architecture(sess, "TEST", len(self.classes), tag='default',
                                anchor_scales=cfg.ANCHOR_SCALES,
                                anchor_ratios=cfg.ANCHOR_RATIOS)

        model = '/home/deckerchan/Workspace/Python/tf-faster-rcnn/output/vgg16/dc_train/default/vgg16_faster_rcnn_iter_2000.ckpt'

        print(('Loading model check point from {:s}').format(model))
        saver = tf.train.Saver()
        saver.restore(sess, model)
        print('Loaded.')

        return sess, net

    def one_shot_detect(self):
        feature = detect(self.fast_rcnn[0], self.fast_rcnn[1], self.classes,
                         cv2.cvtColor(np.array(self.capture.image()), cv2.COLOR_RGB2BGR))
        return feature
