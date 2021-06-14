from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import cv2
import pickle
import imageio
from sklearn.model_selection import train_test_split
import tensorflow as tf
import os.path


CATEGORIES = ['%', '(', ')', '*', '+', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ">", "DOT", 'x', 'y']

def run_prediction():
    result = ''
    i = 0
    previous = 0

    # going through all elements
    f = open("count_images.txt", "r")
    n = int(f.read())

    while i < n:
        istring = str(i)

        if (os.path.isfile("./images/ROI_" + istring + ".png")):
            img = load_img("./images/ROI_" + istring + ".png", grayscale=True, target_size=(28, 28))
            # converting it to array
            img = img_to_array(img)
            img = img.reshape(1, 28, 28, 1)
            # preparing the pixel data
            img = img.astype('float32')
            img = img / 255.0
            model = load_model("Model.model")
            digit = model.predict_classes(img)
            category = CATEGORIES[int(digit[0])]
            if(category == '%'):
                category = '/'
            if (category == "DOT"):
                category = '.'
            result = result + category
            i = i + 1
        elif (os.path.isfile("./images/ROIpow_" + istring + ".png")):
            img = load_img("./images/ROIpow_" + istring + ".png", grayscale=True, target_size=(28, 28))
            # converting it to array
            img = img_to_array(img)
            img = img.reshape(1, 28, 28, 1)
            # preparing the pixel data
            img = img.astype('float32')
            img = img / 255.0
            model = load_model("Model.model")
            digit = model.predict_classes(img)
            # print(CATEGORIES[int(digit[0])])
            category = CATEGORIES[int(digit[0])]
            if (category == '%'):
                category = '/'
            if (category == "DOT"):
                category = '.'
            result = result + category
            i = i + 1
        elif (os.path.isfile("./images/ROIpower_" + istring + ".png")):
            img = load_img("./images/ROIpower_" + istring + ".png", grayscale=True,
                           target_size=(28, 28))
            # converting it to array
            img = img_to_array(img)
            img = img.reshape(1, 28, 28, 1)
            # preparing the pixel data
            img = img.astype('float32')
            img = img / 255.0
            model = load_model("Model.model")
            digit = model.predict_classes(img)
            # print(CATEGORIES[int(digit[0])])
            category = CATEGORIES[int(digit[0])]
            if (category == '%'):
                category = '/'
            if (category == "DOT"):
                category = '.'
            result = result +  ')' + category
            i = i + 1
        elif(os.path.isfile("./images/ROIpowerEND_" + istring + ".png")):
            img = load_img("./images/ROIpowerEND_" + istring + ".png", grayscale=True,
                           target_size=(28, 28))
            # converting it to array
            img = img_to_array(img)
            img = img.reshape(1, 28, 28, 1)
            # preparing the pixel data
            img = img.astype('float32')
            img = img / 255.0
            model = load_model("Model.model")
            digit = model.predict_classes(img)
            # print(CATEGORIES[int(digit[0])])
            category = CATEGORIES[int(digit[0])]
            if (category == '%'):
                category = '/'
            if (category == "DOT"):
                category = '.'
            result = result + category
            result = result + ')'
            i = i + 1
        elif (os.path.isfile("./images/powerSLASH_" + istring + ".png")):
            img = load_img("./images/powerSLASH_" + istring + ".png", grayscale=True,
                           target_size=(28, 28))
            # converting it to array
            img = img_to_array(img)
            img = img.reshape(1, 28, 28, 1)
            # preparing the pixel data
            img = img.astype('float32')
            img = img / 255.0
            model = load_model("Model.model")
            digit = model.predict_classes(img)
            # print(CATEGORIES[int(digit[0])])
            category = CATEGORIES[int(digit[0])]
            if (category == '%'):
                category = '/'
            if (category == "DOT"):
                category = '.'
            result = result + '**' + category
            i = i + 1
        else:
            img = load_img("./images/power_" + istring + ".png", grayscale=True,
                           target_size=(28, 28))
            # converting it to array
            img = img_to_array(img)
            img = img.reshape(1, 28, 28, 1)
            # preparing the pixel data
            img = img.astype('float32')
            img = img / 255.0
            model = load_model("Model.model")
            digit = model.predict_classes(img)
            category = CATEGORIES[int(digit[0])]
            if (category == '%'):
                category = '/'
            if (category not in "+*-()/=>"):
                if (previous not in "+-*()/=>"):
                    result = result + '**' + '(' + category
                else:
                    result = result + category
            else:
                result = result + category
            i = i + 1
        previous = category
    return result
def oneVariable(res):
    # this is supposed to find the x and y value assignment
    # and assign it to the x and y in the expression
    currentS1 = ""
    valueX = ""
    valueY = ""

    if (")" in res):
        # go through array, find ) and get the value
            found = False
            i = 0
            while (found == False):
                if (res[i] == ")"):
                    # )i xi+1 -i+2 >i+3
                    valueX = res[i + 4:]
                    valueY = res[i + 4:]
                    found = True
                else:
                    currentS1 = currentS1 + res[i]
                i += 1
            currentS = ""
            if ("x->" in res):
                for j in range(0, len(currentS1)):
                    if (currentS1[j] == "x"):
                        currentS = currentS + valueX
                    else:
                        currentS = currentS + currentS1[j]
            if ("y->" in res):
                for j2 in range(0, len(currentS1)):
                    if (currentS1[j2] == "y"):
                        currentS = currentS + valueY
                    else:
                        currentS = currentS + currentS1[j2]
            currentS1 = currentS
    else:
        currentS1 = res
    return currentS1

def twoVariables(res):
    # this is supposed to find the x and y value assignment
    # and assign it to the x and y in the expression
    currentS1 = ""
    valueX = ""
    valueY = ""
    count = 0

    if (")" in res):
            expr = res.index(')',0)
            i = 0
            comma = res.index(')', expr+1)
            while i<len(res):
                if (res[i] == ')'):
                    count = count + 1
                if(i < expr):
                    currentS1 = currentS1 + res[i]
                else:
                    if(count == 1 and res[i] == ')'):
                        if('x' in res[expr+1]):
                            valueX = res[i+4:comma]
                            i+=4
                            continue
                        if ('y' in res[expr+1]):
                            valueY= res[i + 4:comma]
                            i += 4
                            continue
                    elif(count == 2 and res[i] == ')'):
                        if('x' in res[comma+1:]):
                            valueX = res[i+4]
                            i += 4
                            continue
                        if ('y' in res[comma+1:]):
                            valueY = res[i + 4]
                            i += 4
                            continue
                i+=1
            currentS = ""
            if(valueX != ""):
                if ("x" in res):
                    for j in range(0, len(currentS1)):
                        if (currentS1[j] == "x"):
                            currentS = currentS + valueX
                        else:
                            currentS = currentS + currentS1[j]
            currentS2 = ""
            if(valueY != ""):
                if ("y" in currentS):
                    for j2 in range(0, len(currentS)):
                        if (currentS[j2] == "y"):
                            currentS2 = currentS2 + valueY
                        else:
                            currentS2 = currentS2 + currentS[j2]
                currentS1 = currentS2
    else:
        currentS1 = res
    return currentS1

try:
    res = run_prediction()
    if('x' in res and 'y' in res):
        if(res.count('>')==2):
            currentS1 = twoVariables(res)
        else:
            currentS1 = oneVariable(res)
    elif('x' in res or 'y' in res):
        currentS1 = oneVariable(res)
    else:
        currentS1 = res
    open('the_result.txt', 'w').close()
    f = open("the_result.txt", "a")
    f.write(str(currentS1))
    f.close()
except SyntaxError as err:
    print("Couldn't chalculate ur expresion")
