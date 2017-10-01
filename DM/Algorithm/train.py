import tensorflow as tf
from tflearn.data_utils import pad_sequences
import numpy as np
import math
from DM.Algorithm.mlp import MLP
from DM.Algorithm.data_helper import loadSamples
import os
import time
import datetime

FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_integer('sample_len', 1138, 'sample len')
tf.app.flags.DEFINE_float('learning_rate', 0.0001, 'learning rate')
tf.app.flags.DEFINE_integer('decay_steps', 5000, 'decay steps')
tf.app.flags.DEFINE_float('decay_rate', 0.85, 'decay rate')
tf.app.flags.DEFINE_float('l2_reg_lambda', 0.0, 'L2 regular para')
tf.app.flags.DEFINE_boolean('allow_soft_placement', True, 'Allow device soft device placement')
tf.app.flags.DEFINE_boolean('log_device_placement', False, 'Log placement of ops on devices')
tf.app.flags.DEFINE_integer('num_epochs', 40, 'number of epochs')
tf.app.flags.DEFINE_integer('batch_size', 64, 'batch_size')
tf.app.flags.DEFINE_integer('print_stats_every', 10, 'Print training stats numbers after this many steps')


def main(_):
    train_x, train_y, train_userid, valid_x, valid_y, valid_userid = loadSamples()
    train_sample_size = len(train_x)
    with tf.Graph().as_default():
        session_conf = tf.ConfigProto(
            allow_soft_placement=FLAGS.allow_soft_placement,
            log_device_placement=FLAGS.log_device_placement)
        session_conf.gpu_options.allow_growth = True
        sess = tf.Session(config=session_conf)
        with sess.as_default(), tf.device('/gpu:1'):
            mlp = MLP(
                FLAGS.sample_len,
                FLAGS.learning_rate,
                FLAGS.decay_steps,
                FLAGS.decay_rate,
                FLAGS.l2_reg_lambda)
            sess.run(tf.global_variables_initializer())
            batch_step = 0
            loss_acc = 0.
            for epoch in range(0, FLAGS.num_epochs):
                print('epoch:' + str(epoch))
                for start, end in zip(range(0, train_sample_size, FLAGS.batch_size),
                                      range(FLAGS.batch_size, train_sample_size, FLAGS.batch_size)):
                    batch_input_x = train_x[start:end]
                    batch_input_y = train_y[start:end]
                    feed_dict = {
                        mlp.input_x: batch_input_x,
                        mlp.input_y: batch_input_y
                    }
                    loss, _ = sess.run([mlp.loss_val, mlp.train_op], feed_dict)
                    loss_acc += loss
                    if batch_step % FLAGS.print_stats_every == 0:
                        print('Epoch:%d\tBatch_Step:%d\tTrain_Loss:%.4f' % (epoch, batch_step, loss / batch_step))
                    batch_step += 1


if __name__ == '__main__':
    tf.app.run()
