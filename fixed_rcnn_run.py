import cv2
import numpy as np
import tensorflow as tf

from capture import Capture
from faster_rcnn.src.model.config import cfg, cfg_from_file, cfg_from_list
from faster_rcnn.src.datasets.factory import get_imdb
from faster_rcnn.src.nets.vgg16 import vgg16
from single_run import detect

tfconfig = tf.ConfigProto(allow_soft_placement=True)
tfconfig.gpu_options.allow_growth = True

# init session
sess = tf.Session(config=tfconfig)
net = vgg16(batch_size=1)



imdb = get_imdb('derek_set_val')
imdb.competition_mode(False)


# load model
net.create_architecture(sess, "TEST", imdb.num_classes, tag='default',
                        anchor_scales=cfg.ANCHOR_SCALES,
                        anchor_ratios=cfg.ANCHOR_RATIOS)

model = '/home/deckerchan/Workspace/Python/tf-faster-rcnn/output/vgg16/dc_train/default/vgg16_faster_rcnn_iter_2000.ckpt'

print(('Loading model check point from {:s}').format(model))
saver = tf.train.Saver()
saver.restore(sess,model)
print('Loaded.')

while True:
    capture = Capture(100, 100, 780, 440)
    im = capture.image()

    # cv2.imshow('frame', cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR))
    # cv2.waitKey(10)
    detect(sess, net, imdb, cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR), wait=1)
