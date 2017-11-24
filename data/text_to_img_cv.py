import re
import cv2
import numpy as np

from converter.romanize import romanize

# 음소를 숫자 데이터로 맵핑
phone_dict = {"-": 16, "a": 19, "e": 21, "i": 23, "o": 25, "u": 27, "h": 30, "b": 34, "v": 35, "p": 36,
              "f": 37, "c": 40, "k": 41, "q": 42, "g": 44, "d": 47, "t": 49, "j": 52, "z": 54,
              "w": 58, "y": 60, "r": 63, "l": 64, "s": 68, "x": 70, "n": 74, "m": 77, "_": 79}


# 텍스트를 이미지로 변환
def textpair_to_image(title1, title2):
    word_list1 = []
    word_list2 = []
    title1_roman = romanize(title1).lower()
    title1_roman_wo_space = re.sub(r" ", r"_-", re.sub(r"[`;<>~0-9\[\]|:+-/.,!?@#$%^*()\'\"]", r" ",
                                                       re.sub(r"&", r" and ", title1_roman)))
    title2_roman = romanize(title2).lower()
    title2_roman_wo_space = re.sub(r" ", r"_-", re.sub(r"[`;<>~0-9\[\]|:+-/.,!?@#$%^*()\'\"]", r" ",
                                                       re.sub(r"&", r" and ", title2_roman)))
    NPOINTS1 = len(title1_roman_wo_space)
    NPOINTS2 = len(title2_roman_wo_space)

    x1 = []
    y1 = []

    x2 = []
    y2 = []

    for a in title1_roman_wo_space:
        word_list1.append(phone_dict[a])

    for b in title2_roman_wo_space:
        word_list2.append(phone_dict[b])

    for i in range(len(word_list1) - 1):
        x1_, y1_ = word_list1[i], word_list1[i + 1]
        x1.append(x1_)
        y1.append(y1_)

    for j in range(len(word_list2) - 1):
        x2_, y2_ = word_list2[j], word_list2[j + 1]
        x2.append(x2_)
        y2.append(y2_)

    length_line1 = 0
    length_line2 = 0

    for i in range(NPOINTS1 - 2):
        line_piece = np.linalg.norm([x1[i + 1] - x1[i], y1[i + 1] - y1[i]])
        length_line1 = length_line1 + line_piece

    for j in range(NPOINTS2 - 2):
        line_piece = np.linalg.norm([x2[j + 1] - x2[j], y2[j + 1] - y2[j]])
        length_line2 = length_line2 + line_piece

    # print(length_line1, length_line2)

    img = np.zeros([96, 96], dtype=np.float64)
    # img3 = np.zeros([96, 96], dtype=np.float64)

    for i in range(NPOINTS1 - 2):
        img1 = cv2.line(img, (x1[i], y1[i]), (x1[i + 1], y1[i + 1]), (255, 255, 255), max(2, int(1000 / length_line1)))

    for j in range(NPOINTS2 - 2):
        img2 = cv2.line(img, (x2[i], y2[i]), (x2[i + 1], y2[i + 1]), (255, 255, 255), max(2, int(1000 / length_line2)))

    img = np.dstack((img1, img2))

    # 직접 확인하고 싶을 경우 img3=0 을 포함하여 확인
    # img = np.dstack((img1, img2, img3))
    # cv2.imshow('image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return img


img = textpair_to_image("헬로우", "마이네임이즈표브")
print(img)
