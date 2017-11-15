import cv2
import numpy as np
import os
from random import shuffle
from tqdm import tqdm

import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

import tensorflow as tf

import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf").get_name()
rc('font', family=font_name)

DATA_DIR = '../data/image_merge'
IMG_SIZE = 64
LR = 0.001

MODEL_NAME = 'trademarks-{}-{}.model'.format(LR, '2conv-basic')


def label_img(img):
    word_label = img.split('.')[-2]
    if word_label == '0':
        return [1, 0]
    elif word_label == '1':
        return [0, 1]
    else:
        pass


def title_img(img):
    title1 = img.split('.')[0]
    title2 = img.split('.')[1]
    return title1, title2


def create_train_test_data():
    all_data = []
    train_data = []
    test_data = []
    for img in tqdm(os.listdir(DATA_DIR)):
        label = label_img(img)
        title1, title2 = title_img(img)
        path = os.path.join(DATA_DIR, img)
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        all_data.append([np.array(img), np.array(label), title1, title2])
    shuffle(all_data)
    try:
        train_data = all_data[:-20]
        shuffle(train_data)
        np.save('train_data.npy', train_data)
        test_data = all_data[-20:]
        shuffle(test_data)
        np.save('test_data.npy', test_data)
    except Exception:
        pass

    return train_data, test_data

train_data, test_data = create_train_test_data()
# train_data = np.load('train_data.npy')
# test_data = np.load('test_data.npy')

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
convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

model = tflearn.DNN(convnet, tensorboard_dir='log')

if os.path.exists('{}.meta'.format(MODEL_NAME)):
    model.load(MODEL_NAME)
    print('model loaded!')

train = train_data[:-20]
validation = train_data[-20:]

X = np.array([i[0] for i in train]).reshape(-1, IMG_SIZE, IMG_SIZE, 3)
Y = [i[1] for i in train]

val_x = np.array([i[0] for i in validation]).reshape(-1, IMG_SIZE, IMG_SIZE, 3)
val_y = [i[1] for i in validation]

model.fit({'input': X}, {'targets': Y}, n_epoch=6, validation_set=({'input': val_x}, {'targets': val_y}),
          snapshot_step=1000, show_metric=True, run_id=MODEL_NAME)

model.save(MODEL_NAME)


fig = plt.figure()

for label, data in enumerate(test_data[:12]):

    img_label = data[1]
    img_data = data[0]
    title1 = data[2]
    title2 = data[3]

    y = fig.add_subplot(3, 4, label + 1)
    orig = img_data
    data = img_data.reshape(IMG_SIZE, IMG_SIZE, 3)
    model_out = model.predict([data])[0]

    if np.argmax(model_out) == 1:
        str_label = 'Non-similar'
    else:
        str_label = 'Similar'

    plt_subtitle = str_label + str(img_label) + "\n" + title1 + ' & ' + title2
    y.imshow(cv2.cvtColor(orig, cv2.COLOR_BGR2RGB))
    plt.title(plt_subtitle)
    y.axes.get_xaxis().set_visible(False)
    y.axes.get_yaxis().set_visible(False)
plt.show()