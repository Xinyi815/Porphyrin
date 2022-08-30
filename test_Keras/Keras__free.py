# first neural network with keras tutorial
import tensorflow as tf
from numpy import loadtxt
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# load the dataset
dataset = loadtxt('total_data_free.txt', delimiter=',')

# split into input (X) and output (y) variables
X = dataset[:, 0:29]
#print(f'X = {X}')
y = dataset[:, 29]

# define the keras model
model = Sequential()
model.add(Dense(30, input_shape=(29,),activation='relu'))
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
historial = model.fit(X, y, epochs=1000, batch_size=18, verbose=True)
print("Model trained!")


# Metrics plots
fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(historial.history['mae'])
axs[0, 0].set_title('MAE')

axs[0, 1].plot(historial.history['cosine_proximity'])
axs[0, 1].set_title('Cosine Proximity')
plt.tight_layout()
#plt.savefig("metrics_free.png")

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


# make predictions with the model
predictions = model.predict(X)
# summarize the first 9 cases
for i in range(10):
    print('%s => %.4f (expected %.4f)' % (X[i].tolist(), predictions[i], y[i]))

# save model and architecture to single file
model.save("model_free.h5")
print("Saved model to disk")

n = list(range(len(X)))
i = [2,3,4,5,6,7,8,9,10]
plt.subplot(212)
plt.title('raw HL and prediction (free)')
plt.plot(i, y[:9], color='blue', marker='o', label='raw data')
plt.plot(i, predictions[:9], color='red', marker='o', label='prediction ')
plt.xlabel('No of porphyrin units')
plt.ylabel('HL gap/eV')
plt.legend()
plt.tight_layout()
plt.savefig("free.png")
