from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from slim.datasets import convert_customer_set

import tensorflow as tf

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string(
    'dataset_dir',
    None,
    'The directory where the output TFRecords and temporary files are saved.')

def main(_):
    if not FLAGS.dataset_dir:
        raise ValueError('You must supply the dataset directory with --dataset_dir')

    convert_customer_set.run(FLAGS.dataset_dir)

if __name__ == '__main__':
  tf.app.run()
