import pytesseract
import numpy as np
import imutils
import cv2
import easyocr
reader = easyocr.Reader(['es'])

def recognize_numbers(crop, psm=7, vote='hard'):
    list_num = [];
    list_conf = []
    image = cv2.imread(crop)
    image = imutils.resize(image, width=300)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    squareKern = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    light = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, squareKern)
    light = cv2.threshold(light, 0, 255,
                          cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F,
    #              dx=1, dy=0, ksize=-1)

    roi = cv2.threshold(light, 0, 255,
                        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    d = reader.readtext(roi,  contrast_ths=0.2, adjust_contrast=0.7, min_size=1, mag_ratio=1)

    if d != []:
       # print('deblured', d)  # (poner subrutina)
        text, conf = d2text(d)
        list_num.append(text)
        list_conf.append(conf)

    if d == [] or conf < 0.999:
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        smooth = cv2.GaussianBlur(gray, (5, 5), 0)

        d = reader.readtext(smooth, contrast_ths=0.2, adjust_contrast=0.7, min_size=1,
                            mag_ratio=1)
        # divide gray by morphology image

        if d != []:
            # print('deblured', d)  # (poner subrutina)
            text, conf = d2text(d)
            list_num.append(text)
            list_conf.append(conf)
        if d == [] or conf < 0.99:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            smooth = cv2.GaussianBlur(gray, (95, 95), 0)
            division = cv2.divide(gray, smooth, scale=255)
            squareKern = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            light = cv2.morphologyEx(division, cv2.MORPH_CLOSE, squareKern)
            light = cv2.threshold(division, 0, 255,
                                  cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            # self.debug_imshow("Light Regions", light, waitKey=True)
            # gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F,
            #              dx=1, dy=0, ksize=-1)

            d = reader.readtext(light, contrast_ths=0.2, adjust_contrast=0.7, min_size=1,
                                mag_ratio=1)
            if d != []:
                # print('deblured', d)  # (poner subrutina)
                text, conf = d2text(d)
                list_num.append(text)
                list_conf.append(conf)

    if d == [] or conf < 0.999:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        smooth = cv2.GaussianBlur(gray, (5, 5), 0)
        d = reader.readtext(smooth, contrast_ths=0.2,  adjust_contrast=0.7, min_size=1,
                            mag_ratio=1)
        # divide gray by morphology image
        if d != []:
            # print('deblured', d)  # (poner subrutina)
            text, conf = d2text(d)
            list_num.append(text)
            list_conf.append(conf)


    list_num = [item for i,item in enumerate(list_num) if list_conf[i] != 0]
    list_conf = [item for i, item in enumerate(list_conf) if list_conf[i] != 0]
   # print('lista no zeros', list_num)
   # print('conf no zeros', list_conf)

    if list_num != [] and vote == 'hard':
        if len(list_num) == 1 and list_conf[0]>=0.5:
           # print('tamaó lista igual 1', len(list_num))
            text = list_num[0]
            conf = list_conf[0]
        elif len(list_num) == 1 and list_conf[0]<0.5:
            text = 0
            conf = 0
        else:
           # print('lista mayora 1',len(list_num))
            text = max(set(list_num), key=list_num.count)
            list_num_a = np.array(list_num)
            list_conf_a = np.array(list_conf)

            if len(set(list_num)) == len(list_num):
                if list_conf[-1]>0.8:
                    text = list_num[-1]  # mas fiable método smooth si los demás no estan en desacuerdo
                    conf = list_conf[-1]
                else:
                   # text = list_num[list_conf == max(list_conf)]
                   text = list_num_a[list_conf_a == max(list_conf_a)][0]
                   conf = max(list_conf_a)

            elif np.array(text).size == 1:

                    conf = max(list_conf_a[list_num_a == text])

            else:

                    text = list_num_a[list_conf_a == max(list_conf_a)][0]
                    conf = max(list_conf_a)

    elif list_num != [] and vote == 'soft':
        """ aquí pesando por probabilidades"""
    else:
        text = 0
        conf = 0

        # VOTING METHOD? CONTAR CUANTAS VECES ME SALE UNO DE LOS NÚMEROS??

    return text, conf


def d2text(d):
    if len(d) == 1:
      #  print(d)
        #if d[0][-2].isdigit():
       # text = d[0][-2]
        #conf = d[0][-1]
        if d[0][-2].isdigit():
            text = d[0][-2]
            conf = d[0][-1]
        elif True in [char.isdigit() for char in d[0][-2]]:
            text = ''.join([i for i in d[0][-2] if i.isdigit()])
            conf = d[0][-1]
        else: #mejro con exception
            text = 0
            conf = 0


    else:
        for item in d:
            if item[-2].isdigit():
                text = item[-2]
                conf = item[-1]
            elif True in [char.isdigit() for char in item[-2]]:
                 text = ''.join([i for i in item[-2] if i.isdigit()])
                 #text = item[-2]
                 conf = item[-1]
            else: # mejro con exception
                text = 0
                conf = 0

    return text, conf