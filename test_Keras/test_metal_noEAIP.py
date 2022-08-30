# first neural network with keras tutorial
import tensorflow as tf
from numpy import loadtxt
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# load the dataset
dataset = loadtxt('Ni_Zn_data.txt', delimiter=',')

# split into input (X) and output (y) variables
X = dataset[:, 0:28]
#print(f'X = {X}')
y = dataset[:, 30]

# define the keras model
model = Sequential()
model.add(Dense(30, input_shape=(28,),activation='relu'))
model.add(Dense(25, ))
model.add(Dense(20, ))
model.add(Dense(15, ))
model.add(Dense(10, ))
model.add(Dense(5,))
model.add(Dense(1,))


# compile the keras model
print('Compiling model...')

metrics=['mse', 'mae', 'mape', 'cosine_proximity']

model.compile(
    loss='mae',
    optimizer='adam', 
    metrics=metrics,
    )

# fit the keras model on the dataset
print('Training model...')
historial = model.fit(X, y, epochs=1000, batch_size=12, verbose=True)
print("Model trained!")

# Metrics plots
fig, axs = plt.subplots(3, 2)
axs[0, 0].plot(historial.history['mse'])
axs[0, 0].set_title('MSE')

axs[0, 1].plot(historial.history['mae'])
axs[0, 1].set_title('MAE')

axs[1, 0].plot(historial.history['mape'])
axs[1, 0].set_title('MAPE')

axs[1, 1].plot(historial.history['cosine_proximity'])
axs[1, 1].set_title('Cosine Proximity')

plt.tight_layout()
#plt.savefig("metrics_metal2.png")

# evaluate the keras model
evaluation = model.evaluate(X, y)
print('======= Metrics ========')
print('Loss: %.3f' % (evaluation[0]))
print('MSE: %.3f' % (evaluation[1]))
print('MAE: %.3f' % (evaluation[2]))
print('MAPE: %.3f' % (evaluation[3]))
print(f'Accuracy: {100 - evaluation[3]}')
print('Cosine proximity: %.3f' % (evaluation[4]))
print('========================')


# make class predictions with the model
#predictions = model.predict(X)
predictions = model.predict(X)
#result = model.predict([[3,126,88,41,235,39.3,0.704,80]])
#print(np.round(result))
#print('%s => %d (expected %d)' % (X.tolist(), predictions, y))
# summarize the first 9 cases
for i in range(9):
    print('%s => %.4f (expected %.4f)' % (X[i].tolist(), predictions[i], y[i]))

# save model and architecture to single file
model.save("model_metal_noEAIP.h5")
print("Saved model to disk")

n = list(range(len(X)))
i = [2,3,4]
plt.subplot(313)
plt.title('raw HL and prediction (metal)')
plt.plot(i, y[:3], color='blue', marker='o', label='raw data')
plt.plot(i, predictions[:3], color='red', marker='o', label='prediction ')
plt.xlabel('No of porphyrin units')
plt.ylabel('HL gap/eV')
plt.legend()
plt.tight_layout()
plt.savefig("metal_noEAIP.png")

# new 2 instances where we do not know the answer: Ni_H_C10_2, Ni_H_C8_6 and Ni_H_C8_10 
Xnew = np.array([[850.067,282,60,0,8,8,0,10,0,0,0,0,0,0,0,8,0,0,6,0,0,0,0,0,0,28,10,2],[2522.171,834,178,0,24,24,0,30,0,0,0,0,0,0,0,24,0,0,16,0,0,0,0,0,0,28,8,6],[3298.223,1090,232,0,32,32,0,40,0,0,0,0,0,0,0,32,0,0,24,0,0,0,0,0,0,28,8,8]])
# make a prediction
ynew = model.predict(Xnew)
# show the inputs and predicted outputs
print("X=%s, Predicted=%s" % (Xnew.tolist(), ynew))
