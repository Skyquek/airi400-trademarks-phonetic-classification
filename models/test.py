import cv2
import numpy as np
import os

import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

import tensorflow as tf

from data.text_to_img_2 import save_pair_image
from converter.romanize import romanize
import re

MAX_LENGTH = 20
LR = 0.001
IMG_SIZE = 224
MODEL_NAME = 'trademarks-{}-{}.model'.format(LR, '2conv-basic')

title1 = input("Title1 EN limit 20, KR limit 7:")
title1_roman = romanize(title1)
title1_input = title1_roman

title2 = input("Title2 EN limit 20, KR limit 7:")
title2_roman = romanize(title2)
title2_input = title2_roman

save_pair_image(title1_input, title2_input, 0)
title1_refine = re.sub(r"[`;&<>~0-9\[\]|:+-/.,!?@#$%^*()\'\"]", r"", title1_input)
title2_refine = re.sub(r"[`;&<>~0-9\[\]|:+-/.,!?@#$%^*()\'\"]", r"", title2_input)

path = 'image_test/' + str(title1_refine[:MAX_LENGTH]) + "." + str(title2_refine[:MAX_LENGTH]) + \
       '.' + str(0) + '.png'

data = []
img = cv2.imread(path, cv2.IMREAD_COLOR)
data.append(np.array(img))

tf.reset_default_graph()

convnet = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 3], name='input')

convnet = conv_2d(convnet, 32, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 64, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 32, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 64, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 32, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 64, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = fully_connected(convnet, 1024, activation='relu')
convnet = dropout(convnet, 0.8)

convnet = fully_connected(convnet, 2, activation='softmax')
convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy',
                     name='targets')

model = tflearn.DNN(convnet, tensorboard_dir='log')

if os.path.exists('{}.meta'.format(MODEL_NAME)):
    model.load(MODEL_NAME)
    print('model loaded!')

model_out = model.predict(data)[0]

if np.argmax(model_out) == 1:
    str_label = 'Non-similar'
else:
    str_label = 'Similar'

print(str_label)