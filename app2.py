import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, Activation
import tensorflow as tf
from sklearn.model_selection import train_test_split
import os
from keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import pickle
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from keras.preprocessing.image import load_img

pickle_in = open("X.pickle","rb")
X = pickle.load(pickle_in)

pickle_in = open("y.pickle","rb")
y = pickle.load(pickle_in)
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.10, shuffle= True)
# acquiring the rows and columns of the image for later use
img_rows=x_train[0].shape[0] # rows of image
img_cols=x_test[0].shape[1] # cols of image
# reshaping the images
x_train=x_train.reshape(x_train.shape[0],img_rows,img_cols,1)
x_test=x_test.reshape(x_test.shape[0],img_rows,img_cols,1)

# normalizing the data set between 0 and 1
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255


# converting class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, 20)
y_test = keras.utils.to_categorical(y_test, 20)

# creating a model
model = Sequential()
# adding layers
model.add(Conv2D(32, (3, 3), padding="same", activation="relu", input_shape=(28,28,1)))
model.add(Conv2D(32, (3, 3), activation="relu"))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.20)) #percentage to cut

# adding some more layers
model.add(Conv2D(64, (3, 3), padding="same", activation="relu"))
model.add(Conv2D(64, (3, 3), activation="relu"))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.20)) #percentage to cut

# flattening + last layers
model.add(Flatten())
model.add(Dense(512, activation="relu"))
model.add(Dropout(0.50)) #percentage to cut
model.add(Dense(20, activation="softmax"))
# compiling
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
# training the data
history = model.fit(x_train, y_train, batch_size=28, epochs=30,validation_data=(x_test, y_test))
# saving the model
model.save("Model.model")

# weights how the network actually works; save weights
model.save_weights("model_weights.h5")
def plot_metric(metric):
	plt.plot(range(30), history.history[metric], color="#FF6F00")
	plt.title(metric)
	plt.show()


plot_metric("accuracy")
plot_metric("loss")
plot_metric("val_loss")
plot_metric("val_accuracy")
# evaluating the model
model.evaluate(x_test, y_test)

# Visualize training results with matplotlib
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(len(acc))

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()