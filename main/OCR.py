import pytesseract
import numpy as np
import time
import imutils
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import math
from difflib import SequenceMatcher
from PIL import Image
#import tensorflow as tf
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import cv2
from PIL import Image
import numpy as np
import pandas as pd
import string
pytesseract.pytesseract.tesseract_cmd = r'C:\\OCR\\tesseract.exe'


def process_image(iamge_name, lang_code):
    return pytesseract.image_to_string(Image.open(iamge_name), lang=lang_code)


def print_data(data):
    print(data)


def output_file(filename, data):
    file = open(filename, "w+")
    file.write(data)
    file.close()


def clear_image(directory):
    im1 = Image.open(str(directory))
    im1.save(r'TESTER.png')

    foo = Image.open("TESTER.png")

    # I downsize the image with an ANTIALIAS filter (gives the highest quality)
    foo = foo.resize((int(foo.size[0]*1.1), int(foo.size[1])), Image.ANTIALIAS)
    foo.save("TESTER.png", quality=95)

    gray_image = cv2.imread('TESTER.png')

    # Sharpness Filter
    kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, 0]])
    im = cv2.filter2D(gray_image, -1, kernel)

    rgb_planes = cv2.split(im)

    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(
            diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)

    result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)
    plt.imsave('TESTER.png', result_norm)

    # Open the input image as numpy array, convert to greyscale and drop alpha
    pixvals = np.array(Image.open("TESTER.png").convert("L"))

    minval = np.percentile(pixvals, 2)
    maxval = np.percentile(pixvals, 98)
    pixvals = np.clip(pixvals, minval, maxval)
    pixvals = ((pixvals - minval) / (maxval - minval)) * 255
    contrast = Image.fromarray(pixvals.astype(np.uint8))
    plt.imsave('TESTER.png', contrast)

    return contrast


def Get_Ingredients(directory, ingredients):
    clear = clear_image(directory)
    # The clear image is stored in the TESTER.jpeg file
    data_eng = process_image('TESTER.png', "eng")

    # print(data_eng)
    data2 = ([i for item in [data_eng] for i in item.split(',')])
    data3 = []
    for x in data2:
        for y in x.split(' '):
            data3.append(y)
    data2 = data3

    col_list = ["Ingredients"]
    df = pd.read_csv(ingredients, usecols=col_list)
    Ingredients_List = []
    char_ignore = '.*[](): '
    ingredients_ignore = ['vitamin', 'fat', 'protein', 'carbohydrate', 'folic', 'acid', 'niacin', 'iron', 'energy',
                          'false', 'minerals', 'ingredients', 'and', 'contain', 'total', 'cholesterol', 'partially', 'natural', 'lessthan',
                          'preservatives', 'hydrogenated', 'calcium', 'starch', 'preservative', 'potassium', 'stabilizer', 'xanthan', 'gum',
                          'sequestrant', 'disodium', 'edta', 'carotene']
    for x in range(len(df['Ingredients'])):
        ing = df['Ingredients'][x]
        if type(ing) == str:
            for y in ing.split(','):
                y = ''.join([i for i in y if i.isalpha()]).replace(' ', '')
                every = [y, y.upper(), y.lower()]
                if len(set(every).intersection(set(Ingredients_List))) == 0 and len(y) > 2 and y[0] not in char_ignore and y[-1] not in char_ignore and len(y) < 15 and list(filter((y.lower()+'prefix').startswith, ingredients_ignore)) == [] and list(filter((y.lower()+'prefix').startswith, Ingredients_List)) == []:
                    Ingredients_List.append(y.lower())
    SET_ING = set(Ingredients_List)
    output = []
    for x in range(len(data2)):
        temp = ''
        temp_lst = []

        for y in data2[x].split('\n'):
            for z in range(len(y)):
                if y[z].isalpha():
                    temp += y[z]
            temp_lst.append(temp)
        # print(temp_lst)
        for i in temp_lst:
            white = i.replace(' ', '')
            for j in Ingredients_List:
                if (SequenceMatcher(a=i.lower(), b=j.lower()).ratio() == 1 or SequenceMatcher(a=white.lower(), b=j.lower()).ratio() == 1) and i.lower() not in output:
                    output.append(i.lower())
            # if set([i.lower(),white.lower()]).intersection(SET_ING)  and i.lower() not in output:
            #    output.append(i.lower())
    return output
# string manipulation is left on some grounds.


#print(Get_Ingredients('images/cornflake.png', 'ingredients.csv'))
#print(Get_Ingredients('images/pita_bread.png', 'ingredients.csv'))
#print(Get_Ingredients('images/popcorn.png', 'ingredients.csv'))
#print(Get_Ingredients('images/mayo.png', 'ingredients.csv'))
