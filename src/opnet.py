import glob

import numpy as np
import tensorflow as tf


class OpNet(object):
    def __init__(self, feature_number, model_path, learn_rate=0.0001):

        self.model_path = model_path
        self.sess = None
        self.feature_number = feature_number
        self.config = tf.ConfigProto()
        self.config.gpu_options.allow_growth = True
        self.learn_rate = learn_rate
        self.init, self.logist, self.loss, self.optimize = self.get_network()

        self.saver = tf.train.Saver()

        pass

    def _fc_layer(self, input_layer, input_nodes, output_nodes, name, activation=None):

        weight = tf.Variable(tf.truncated_normal([input_nodes, output_nodes]), name=str.format("fc_{0}_weight", name))

        bias = tf.Variable(tf.truncated_normal([output_nodes]), name=str.format("fc_{0}_bias", name))

        if activation:
            layer = activation(tf.add(tf.matmul(input_layer, weight), bias), name=str.format("fc_{0}_bias", name))
        else:
            layer = tf.add(tf.matmul(input_layer, weight), bias, name=str.format("fc_{0}_bias", name))

        return layer

    def get_network(self, depth=5, nodes=100):

        input_plh = tf.placeholder(tf.float32, [None, self.feature_number], name='input_plh')
        mouse_locations_plh = tf.placeholder(tf.float32, [None, 4], 'mouse_locations_plh')

        net = self._fc_layer(input_plh, input_plh.shape[-1].value, nodes, '1', tf.nn.relu)

        for i in range(1, depth - 1):
            net = self._fc_layer(net, nodes, nodes, str(i), tf.nn.relu)

        logist = self._fc_layer(net, nodes, mouse_locations_plh.shape[-1].value, 'logist')

        loss = tf.reduce_max(tf.abs(logist - mouse_locations_plh))

        opt = tf.train.AdamOptimizer(self.learn_rate).minimize(loss)

        init = tf.global_variables_initializer()

        return init, logist, loss, opt

    def start(self, sess=None):
        if self.sess is not None:
            raise RuntimeError("Session already set.")

        if sess:
            self.sess = sess
        else:
            self.sess = tf.Session(config=self.config)

        if glob.glob(self.model_path + '*'):
            print(str.format("Restored from {0}", self.model_path))
            self.saver.restore(self.sess, self.model_path)
        else:
            print("Initiallize variables")
            self.sess.run(self.init)

    def train_data_set(self, dataset, iter, batch_size=1):

        # [(features,press_loc,release_loc)]

        for feature, press_loc, release_loc in dataset:
            loc = np.concatenate([np.asarray(press_loc), np.asarray(release_loc)])

            loss = self.sess.run(self.loss, {'input_plh:0': feature, 'mouse_locations_plh:0': loc})

            print(str.format("trained data! Loss:{0}", loss))

        self.saver.save(self.sess, self.model_path)

    def train_data(self, feature, press_loc, release_loc):

        feature = np.expand_dims(feature, axis=0)

        loc = np.concatenate([np.asarray(press_loc), np.asarray(release_loc)])

        loc = np.expand_dims(loc, axis=0)

        loss, _ = self.sess.run([self.loss, self.optimize], {'input_plh:0': feature, 'mouse_locations_plh:0': loc})

        print(str.format("trained data! Loss:{0}", loss))

    def save(self):
        self.saver.save(self.sess, self.model_path)

    def predict(self, feature):
        feature = np.expand_dims(feature, axis=0)

        log = self.sess.run(self.logist, {'input_plh:0': feature})

        return log


if __name__ == '__main__':
    feature1 = [0, 0, 0, 0, 0]
    log1 = [200, 200, 400, 400]

    feature2 = [0, 1, 0, 0, 0]
    log2 = [200, 400, 400, 400]

    feature3 = [0, 0, 1, 0, 0]
    log3 = [200, 200, 600, 400]

    op = OpNet(5, './train/model.ckpt')
    op.start()
    print(op.predict(feature3))

    # while True:
    #     op.train_data(feature1, (log1[0], log1[1]), (log1[2], log1[3]))
    #     op.train_data(feature2, (log2[0], log2[1]), (log2[2], log2[3]))
    #     op.train_data(feature3, (log3[0], log3[1]), (log3[2], log3[3]))
    #     op.save()
