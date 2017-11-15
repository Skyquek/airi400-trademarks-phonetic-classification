from converter.romanize import romanize
import re
import matplotlib.pyplot as plt
import numpy as np
import cv2
import scipy.misc
import math

phone_dict = {"-": 0, "a": 3, "e": 4, "i": 5, "o": 6, "u": 7, "h": 8, "b": 11, "v": 12, "p": 13,
              "f": 14, "c": 17, "k": 18, "q": 19, "g": 20, "d": 23, "t": 24, "j": 27, "z": 28,
              "w": 31, "y": 32, "r": 35, "l": 36, "s": 39, "x": 40, "n": 43, "m": 44, "_": 47}

MAX_LENGTH = 20


def text_to_image(title):
    word_list = []
    title_roman = romanize(title).lower()
    title_roman_wo_space = re.sub(r" ", r"_-", re.sub(r"[`;<>~0-9\[\]|:+-/.,!?@#$%^*()\'\"]", r" ",
                                                      re.sub(r"&", r" and ", title_roman)))
    NPOINTS = MAX_LENGTH + 1
    x = []
    y = []

    len_title_roman = len(title_roman_wo_space)

    if len_title_roman < MAX_LENGTH:
        spare_space = MAX_LENGTH - len_title_roman
        for a in (str("-") + title_roman_wo_space + str("_" * (spare_space + 2))):
            try:
                word_list.append(phone_dict[a])
            except:
                pass

    for i in range(len(word_list) - 1):
        x_, y_ = word_list[i], word_list[i + 1]
        i += 1
        x.append(x_)
        y.append(y_)

    plt.figure(figsize=(2.24, 2.24))

    for i in range(NPOINTS - 1):
        plt.plot(x[i:i + 2], y[i:i + 2], alpha=float(NPOINTS - 1 - i) / (NPOINTS - 1),
                 linewidth=5 * math.log10(1000. / len_title_roman) * float(NPOINTS - 1 - i) / (NPOINTS - 1),
                 color='black')
        plt.plot(47, 47, alpha=0.00000000001)
        plt.axis('off')
        filename = "image/" + title + ".png"
        plt.savefig(filename)
        img = cv2.imread(filename, 0)
        img = (img * -1 + 255.) / 255.
        scipy.misc.imsave(filename, img)


def textpair_to_image(title1, title2):
    title1_roman = romanize(title1).lower()
    title2_roman = romanize(title2).lower()
    title1_roman_wo_space = re.sub(r" ", r"_-", re.sub(r"[`;<>~0-9\[\]|:+-/.,!?@#$%^*()\'\"]", r"",
                                                       re.sub(r"&", r" and ", title1_roman)))
    title2_roman_wo_space = re.sub(r" ", r"_-", re.sub(r"[`;<>~0-9\[\]|:+-/.,!?@#$%^*()\'\"]", r"",
                                                       re.sub(r"&", r" and ", title2_roman)))
    NPOINTS1 = MAX_LENGTH + 1
    NPOINTS2 = MAX_LENGTH + 1

    img3 = np.zeros([224, 224], dtype=np.float64)

    word1_list = []
    word2_list = []
    x1 = []
    y1 = []
    x2 = []
    y2 = []

    len_title1_roman = len(title1_roman_wo_space)
    len_title2_roman = len(title2_roman_wo_space)

    if len_title1_roman < MAX_LENGTH and \
                    len_title2_roman < MAX_LENGTH:
        spare_space1 = MAX_LENGTH - len_title1_roman
        spare_space2 = MAX_LENGTH - len_title2_roman

        for a in (str("-") + title1_roman_wo_space + str("_" * (spare_space1 + 2))):
            try:
                word1_list.append(phone_dict[a])
            except:
                pass

        for a in (str("-") + title2_roman_wo_space + str("_" * (spare_space2 + 2))):
            try:
                word2_list.append(phone_dict[a])
            except:
                pass

        for i in range(len(word1_list) - 1):
            x_, y_ = word1_list[i], word1_list[i + 1]
            i += 1
            x1.append(x_)
            y1.append(y_)

        for i in range(len(word2_list) - 1):
            x_, y_ = word2_list[i], word2_list[i + 1]
            i += 1
            x2.append(x_)
            y2.append(y_)

        plt.figure(figsize=(2.24, 2.24))

        for i in range(NPOINTS1 - 1):
            plt.plot(x1[i:i + 2], y1[i:i + 2], alpha=float(NPOINTS1 - 1 - i) / (NPOINTS1 - 1),
                     linewidth=5 * math.log10(1000. / len_title1_roman) * float(NPOINTS1 - 1 - i) / (NPOINTS1 - 1),
                     color='black')
            plt.plot(47, 47, alpha=0.00000000001)
            plt.axis('off')
            title1_refine = re.sub(r"[`;&<>~0-9\[\]|:+-/.,!?@#$%^*()\'\"]", r"", title1)
            filename1 = "image/" + str(title1_refine) + ".png"
            plt.savefig(filename1)
            img1 = cv2.imread(filename1, 0)
            img1 = (img1 * -1 + 255.) / 255.
            scipy.misc.imsave(filename1, img1)
        # print("img1: ", img1.shape)
        plt.close()

        plt.figure(figsize=(2.24, 2.24))

        for j in range(NPOINTS2 - 1):
            plt.plot(x2[j:j + 2], y2[j:j + 2], alpha=float(NPOINTS2 - 1 - j) / (NPOINTS2 - 1),
                     linewidth=5 * math.log10(1000. / len_title2_roman) * float(NPOINTS2 - 1 - j) / (NPOINTS2 - 1),
                     color='black')
            plt.plot(47, 47, alpha=0.00000000001)
            plt.axis('off')
            title2_refine = re.sub(r"[`;&<>~0-9\[\]|:+-/.,!?@#$%^*()\'\"]", r"", title2)
            filename2 = "image/" + str(title2_refine) + ".png"
            plt.savefig(filename2)
            img2 = cv2.imread(filename2, 0)
            img2 = (img2 * -1 + 255.) / 255.
            scipy.misc.imsave(filename2, img2)
        # print("img2: ", img2.shape)
        plt.close()

        img = np.dstack((img1, img2, img3))

        return img

    else:
        pass


def save_pair_image(title1, title2, label):
    try:
        img = textpair_to_image(title1, title2)
        title1_refine = re.sub(r"[`;&<>~0-9\[\]|:+-/.,!?@#$%^*()\'\"]", r"", title1)
        title2_refine = re.sub(r"[`;&<>~0-9\[\]|:+-/.,!?@#$%^*()\'\"]", r"", title2)
        scipy.misc.imsave(
            'image_test/' + str(title1_refine[:MAX_LENGTH]) + "." + str(title2_refine[:MAX_LENGTH]) + '.' + str(label) + '.png', img)
    except Exception:
        pass