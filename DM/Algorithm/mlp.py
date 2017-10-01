import tensorflow as tf
import numpy as np
from tensorflow.python.framework import ops
from tensorflow.python.ops import gen_nn_ops


class MLP(object):
    def __init__(self, sample_len, learning_rate, decay_steps, decay_rate, l2_reg_lambda):
        self.sample_len = sample_len
        self.learning_rate = learning_rate
        self.global_step = tf.Variable(0, trainable=False, name='Global_Step')
        self.decay_steps = decay_steps
        self.decay_rate = decay_rate
        self.l2_reg_lambda = l2_reg_lambda
        self.input_x = tf.placeholder(tf.float32, [None, sample_len], name='input_x')
        self.input_y = tf.placeholder(tf.float32, [None, 1], name='input_y')
        self.logits = self.inference()
        self.loss_val = self.loss()
        self.train_op = self.train()

    def inference(self):
        w1 = tf.get_variable(
            'weights_w1',
            shape=[self.sample_len, 10000],
            initializer=tf.contrib.layers.xavier_initializer())
        b1 = tf.Variable(tf.constant(0.1, shape=[10000]), name='b')
        hidden = tf.nn.xw_plus_b(self.input_x, w1, b1, name='hidden1')

        hidden = tf.sigmoid(hidden)  # 各神经元的激活函数

        w = tf.get_variable(
            'weights_w',
            shape=[10000, 1],
            initializer=tf.contrib.layers.xavier_initializer())

        logits = tf.matmul(hidden, w, name='logits')
        logits = tf.sigmoid(logits)
        return logits

    def loss(self):
        print(self.logits.shape)
        print(self.input_y.shape)
        mse = tf.reduce_mean(tf.square(self.logits - self.input_y))
        l2_losses = tf.add_n(
            [tf.nn.l2_loss(v) for v in tf.trainable_variables() if 'weights' in v.name]) * self.l2_reg_lambda
        mse = mse + l2_losses
        return mse

    def train(self):
        self.decay_learning_rate = tf.train.exponential_decay(self.learning_rate, self.global_step, self.decay_steps,
                                                              self.decay_rate, staircase=True)
        train_op = tf.contrib.layers.optimize_loss(self.loss_val, global_step=self.global_step,
                                                   learning_rate=self.decay_learning_rate, optimizer='Adam')
        return train_op
