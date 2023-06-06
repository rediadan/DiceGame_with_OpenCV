import cv2
import numpy as np


def lab_equalizer(img, new_channel):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l,a,b =  cv2.split(lab)
    merged_lab = cv2.merge((new_channel,a,b))
    bgr_img = cv2.cvtColor(merged_lab, cv2.COLOR_LAB2BGR)
    return bgr_img


cap = cv2.VideoCapture(0)


while True:
    ret, image = cap.read()
    if ret == False:
        break

    image_copy = image.copy()

    gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    clahe_applied_perceived_channel = clahe.apply(gray)
    lab_equalized_img = lab_equalizer(image_copy, clahe_applied_perceived_channel)

    # 컨투어 검출하기
    gray = cv2.cvtColor(lab_equalized_img, cv2.COLOR_BGR2GRAY)
    t, binary = cv2.threshold(gray, -1, 255,  cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(binary,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)


    dict_i = {}

    # 주사위를 검출한 컨투어를 찾습니다.
    for i, (c,h) in enumerate(zip(contours,hierarchy[0])):

        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.intp(box)

        p1 = box[0]
        p2 = box[1]
        p3 = box[2]
       
        dist1 = np.linalg.norm(p1-p2)
        dist2 = np.linalg.norm(p2-p3)

        if dist2 == 0:
            dist2 = 0.000001

        if dist1/dist2 > 0.6 and dist1/dist2 < 1.5:         
            if h[3] == -1:
                dict_i[i] = []


    # 주사위 눈을 검출한 컨투어를 찾습니다.
    total_pips = []
    for i, (c,h) in enumerate(zip(contours,hierarchy[0])):
        if h[3] in dict_i.keys():

            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.intp(box)

            area = cv2.contourArea(c)

            p1 = box[0]
            p2 = box[1]
            p3 = box[2]
           
            dist1 = np.linalg.norm(p1-p2)
            dist2 = np.linalg.norm(p2-p3)

            if dist2 == 0:
                dist2 = 0.000001

            print(i, dist1*dist2,  area)

            if dist1/dist2 > 0.6 and dist1/dist2 < 1.5 and 100 < area:
               
                dict_i[h[3]].append(i)
                total_pips.append(i)

    list_del = []
    for key in dict_i.keys():
        if len(dict_i[key]) == 0:
            list_del.append(key)

    for del_item in list_del:
        del dict_i[del_item]

    print('주사위 목록')
    print(dict_i)


    for index, (c,h) in enumerate(zip(contours,hierarchy[0])):
       
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
       
        x, y, _, _ = cv2.boundingRect(c)

       
        # 주사위 눈 리스트 생성
        list_item = []
        for i in dict_i.values():
            list_item = list_item  + i
       

        if index in dict_i.keys() or index in list_item:
           
            # 주사위와 주사위 눈을 그려줌
            cv2.drawContours(image_copy, [box], 0, (255, 0, 150), 3)
           
            # 주사위 눈 개수 출력
            if index in dict_i and len(dict_i[index]) > 0:
                cv2.putText(image_copy,
                            str(len(dict_i[index])),
                            (x+100, y-5),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            2,
                            (0, 0, 255),
                            2,
                        cv2.LINE_AA)

            # 컨투어 인덱스 출력
            cv2.putText(image_copy,
                        str(index),
                        (x+20, y-5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (200, 140, 140),
                        1,
                        cv2.LINE_AA)


    # 전체 주사위 눈 개수 출력
    cv2.putText(image_copy,
                f'total = {len(total_pips)}',
                (50,50),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (0, 0, 255),
                2,
                cv2.LINE_AA)


    # binary = cv2.resize(binary, None, fx=0.5, fy=0.5)
    # image_copy = cv2.resize(image_copy, None, fx=0.5, fy=0.5)

    cv2.imshow('binary', binary)
    cv2.imshow('result', image_copy)
    key = cv2.waitKey(1)

    if key == 27:
        break