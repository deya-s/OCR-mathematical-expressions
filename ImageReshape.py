import os
import numpy as np
from keras.preprocessing.image import load_img
from PIL import Image
import tensorflow as tf
import glob
import matplotlib.pyplot as plt
import cv2
from tqdm import tqdm
from keras.preprocessing.image import img_to_array

DATADIR = "kaggle/"

CATEGORIES = ['%', '(', ')', '*', '+', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ">", "DOT", 'x', 'y']
training_data = []
for category in CATEGORIES:
    print("loading..")
    class_num = CATEGORIES.index(category)
    path = os.path.join(DATADIR, category)
    for img in tqdm(os.listdir(path)):
        try:
            img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
            new_array = cv2.resize(img_array, (28, 28))
            training_data.append([new_array, class_num])
        except Exception as e:
            pass

import random

random.shuffle(training_data)
X = []
y = []

for features, label in training_data:
    X.append(features)
    y.append(label)
X = np.array(X)
y = np.array(y)

import pickle

pickle_out = open("X.pickle", "wb")
pickle.dump(X, pickle_out)
pickle_out.close()

pickle_out = open("y.pickle", "wb")
pickle.dump(y, pickle_out)
pickle_out.close()

# pickle_in = open("X.pickle","rb")
# X = pickle.load(pickle_in)

# pickle_in = open("y.pickle","rb")
# y = pickle.load(pickle_in)
