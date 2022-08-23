# first neural network with keras tutorial
import tensorflow as tf
from numpy import loadtxt
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model

# load model
model = load_model('model_metal.h5')

dataset2 = loadtxt('total_data_TPP.txt', delimiter=',')
# new instance where we do not know the answer
Xnew = dataset2[:, 0:30]
# make a prediction
ynew = model.predict(Xnew)
# show the inputs and predicted outputs
print("X=%s, Predicted=%s" % (Xnew, ynew))
